
"""
Created on 04.04.2016

:author: Andrej Nussdorfer

Tuleap REST API Client for Python
Copyright (c) Djuro Drljaca, All rights reserved.

This Python module is free software; you can redistribute it and/or modify it under the terms of the
GNU Lesser General Public License as published by the Free Software Foundation; either version 3.0
of the License, or (at your option) any later version.

This Python module is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this library. If
not, see <http://www.gnu.org/licenses/>.
"""

import sys, os, csv

from Tuleap.RestClient.Commons import FieldValues, FieldValuesFormat, LinkFollowing
from Tuleap.RestClient.Connection import Connection
from Tuleap.RestClient.Trackers import Tracker
from Tuleap.RestClient.Reports import Reports
from Tuleap.RestClient.Artifacts import Artifacts
from Tuleap.RestClient.ArtifactParser import ArtifactParser


# Public -------------------------------------------------------------------------------------------
class ReportGenerator(object):
    """
    Crawls the artifact tree and generates a csv report file

    Fields type information:
    :type __data: list[list[string]]
    :type __header: list[string]
    :type __max_depth: int
    :type __total_depth: int
    :type __link_following: Tuleap.RestClient.Commons.LinkFollowing
    :type __connection: Tuleap.RestClient.Connection.Connection
    :type __trackers_api: Tuleap.RestClient.Trackers.Tracker
    :type __reports_api: Tuleap.RestClient.Reports.Reports
    :type __trackers_api: Tuleap.RestClient.Artifacts.Artifacts

    """
    def __init__(self, connection):
        """
        Constructor

        :param connection: the connection used to acces the tulip server
        :type connection: Tuleap.RestClient.Connection.Connection

        """
        self.__data = []
        self.__header = []
        self.__max_depth = -1
        self.__total_depth = -1
        self.__link_following = LinkFollowing.No
        self.__connection = connection
        self.__trackers_api = Tracker(self.__connection)
        self.__reports_api = Reports(self.__connection)
        self.__artifacts_api = Artifacts(self.__connection)

    def handle_tracker(self, tracker_chain, link_following):
        """
        Crawl the artifact tree starting with the first tracker in the tracker chain

        :param tracker_chain: the chain of child trackers that need to be followed by the artifact crawler
        :type tracker_chain: list[int]
        :param link_following: he rule that defines how the crawler follows artifact links
        :type link_following: Tuleap.RestClient.Commons.LinkFollowing
        """
        self.__data.clear()
        self.__header.clear()
        self.__max_depth = -1
        self.__total_depth = len(tracker_chain)
        if not isinstance(link_following, LinkFollowing):
            raise Exception("Error: invalid link following rule")
        self.__link_following = link_following
        art_lst_limit = 10
        art_lst_offset = 0
        report_line = []

        while True:
            success = self.__trackers_api.request_artifact_list(tracker_chain[0], FieldValues.All, art_lst_limit,
                                                                art_lst_offset)
            if success:
                art_lst_offset += art_lst_limit
                artifact_lst = self.__trackers_api.get_data()
                if len(artifact_lst) == 0:
                    break
                for art_tmp in artifact_lst:
                    self.__handle_artifact(art_tmp, [], report_line, tracker_chain)

    def get_data(self):
        """
        Get the report data
        """
        return self.__data

    def get_header(self):
        """
        Get the report header
        """
        return self.__header

    def save_artifact_trace(self, file_name):
        """
        Save the report into a csv file.

        :param file_name: The full file name for the report file
        :type file_name: str

        :return Success or failure
        :rtype bool
        """
        header_length = len(self.__header)
        if header_length == 0:
            return False
        with open(file_name, "w+") as report_file:
            csv.register_dialect('my_dialect', delimiter=';', quoting=csv.QUOTE_ALL, doublequote=True,
                                 quotechar='\"', escapechar='\\', lineterminator='\r')
            report_writer = csv.writer(report_file, dialect='my_dialect')
            report_writer.writerow(self.__header)
            for tmp_row in self.__data:
                if len(tmp_row) < header_length:
                    tmp_row.extend([""]*(header_length - len(tmp_row)))
                report_writer.writerow(tmp_row)
        return True


# Private ------------------------------------------------------------------------------------------

    def __end_of_crawl(self, depth, parser):
        go_forward = ((self.__link_following == LinkFollowing.Forward) or (self.__link_following == LinkFollowing.All)) and parser.has_links()
        go_backwards = ((self.__link_following == LinkFollowing.Reverse) or (self.__link_following == LinkFollowing.All)) and parser.has_reverse_links()
        bottom_reached = depth == self.__total_depth
        return (not (go_forward or go_backwards)) or bottom_reached

    def __crawl_forward(self):
        return (self.__link_following == LinkFollowing.Forward) or (self.__link_following == LinkFollowing.All)

    def __crawl_backward(self):
        return (self.__link_following == LinkFollowing.Reverse) or (self.__link_following == LinkFollowing.All)

    def __handle_artifact(self, art_item, rep_head_fragment, rep_line, child_track_lst):
        """
        Handle the current artifact

        :param dict art_item: The current artifact data
        :param list[str] rep_head_fragment: The current report header. It will grow as the crawler descends through
        the artifact tree.
        :param list[str] rep_line: The current state of the report line, based on all the previous artifacts.
        :param list[int] child_track_lst: The list of children tracker IDs

        :return: success: Success or failure
        :rtype: bool
        """
        succ = False
        art_parser = ArtifactParser(art_item, child_track_lst[1:], self.__link_following)
        vals = art_parser.get_values()

        tmp_line = list(rep_line)
        tmp_head = list(rep_head_fragment)
        current_depth = self.__total_depth - len(child_track_lst)

        if current_depth > self.__max_depth:
            for tmp_item in vals:
                self.__header.append(str(art_parser.get_tracker_id()) + "_" + tmp_item["label"])
            self.__max_depth = current_depth

        for tmp_item in vals:
            tmp_line.append(tmp_item["value"])

        if self.__end_of_crawl(current_depth, art_parser):
            self.__data.append(tmp_line)
        else:
            if self.__crawl_forward() and art_parser.has_links():
                for tmp_art_id in art_parser.get_links():
                    succ = self.__artifacts_api.request_artifact(tmp_art_id, FieldValuesFormat.All)
                    if succ:
                        tmp_art_item = self.__artifacts_api.get_data()
                        self.__handle_artifact(tmp_art_item, tmp_head, tmp_line, child_track_lst[1:])
            if self.__crawl_backward() and art_parser.has_reverse_links():
                for tmp_art_id in art_parser.get_reverse_links():
                    succ = self.__artifacts_api.request_artifact(tmp_art_id, FieldValuesFormat.All)
                    if succ:
                        tmp_art_item = self.__artifacts_api.get_data()
                        self.__handle_artifact(tmp_art_item, tmp_head, tmp_line, child_track_lst[1:])
        return True
