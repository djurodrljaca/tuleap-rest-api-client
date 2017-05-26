"""
Created on 17.03.2016

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

from Tuleap.RestClient.ValueParser import ValueParser
from Tuleap.RestClient.Commons import LinkFollowing
from Tuleap.RestClient.utils import at_least_python_3
# Public -------------------------------------------------------------------------------------------


class ArtifactParser(object):
    """
    Parses the artifact and extract the relevant data

    Fields type information:
    :type __artifact: dict
    :type __project_id: int
    :type __tracker_id: int
    :type __values: list[dict]
    :type __links: list[int]
    :type __reverse_links: list[int]
    :type __valid: bool
    :type __link_following: Tuleap.RestClient.Commons.LinkFollowing
    """

    def __init__(self, item, tracker_list=[], link_following=LinkFollowing.No):
        """
        Constructor

        :param item: the artifact item to ber parsed
        :type item: dict
        :param tracker_list: the list of child trackers to be crawled
        :type tracker_list: list[int]
        :param link_following: how to follow the artifact links
        :type link_following: Tuleap.RestClient.Commons.LinkFollowing

        """
        self.__artifact = item
        self.__project_id = -1
        self.__tracker_id = -1
        self.__values = []
        self.__links = []
        self.__reverse_links = []
        self.__valid = False
        if not isinstance(link_following, LinkFollowing):
            raise Exception("Error: invalid link following rule")
        self.__link_following = link_following
        if len(tracker_list) > 0:
            self.__child_id = tracker_list[0]
        else:
            self.__link_following = LinkFollowing.No
            self.__child_id = -1

        self.__valid = self.__parse_item()

    def is_valid(self):
        """
        Check whether the supplied item was convertible to string

        :return: item conversion validity
        :rtype: bool
        """
        return self.__valid

    def get_project_id(self):
        """
        Get the id of the artifacts project

        :return: artifacts project id
        :rtype: int
        """
        return self.__project_id

    def get_tracker_id(self):
        """
        Get the id of the artifacts tracker

        :return: artifacts tracker id
        :rtype: int
        """
        return self.__tracker_id

    def get_values(self):
        """
        Get the dictionary of all supported values found in the artifact

        :return: list of values
        :rtype: list[dict]
        """
        return self.__values

    def get_links(self):
        """
        Get the list of all artifact ids the current artifact links to

        :return: list of direct artifact links
        :rtype: list[int]
        """
        return self.__links

    def has_links(self):
        """
        Check whether the artifact has links to other artifacts

        :return: True if the artifact links to others
        :rtype: bool
        """
        return len(self.__links) > 0

    def get_reverse_links(self):
        """
        Get the list of all ids of the artifacts that link to this

        :return: list of reverse artifact links
        :rtype: list[int]
        """
        return self.__reverse_links

    def has_reverse_links(self):
        """
        Check whether other artifacts have links to the current artifact

        :return: True if the artifact is linked from others
        :rtype: bool
        """
        return len(self.__reverse_links) > 0

# Private-------------------------------------------------------------------------------------------

    def __parse_item(self):
        """
        Parse the current artifact item.
        :return: Parsing status. True if successful, False otherwise.
        :rtype: boolean
        """
        # Extract the project ID
        if self.__extract_project() == False:
            return False
        # Extract the tracker ID
        if self.__extract_tracker() == False:
            return False
        # Extract the artifact values
        self.__extract_values()

        return True

    def __extract_project(self):
        """
        Search for and extract the artifact project ID.

        :return: Extraction status. true if successful.
        :rtype: boolean
        """
        self.__valid = False
        if "project" in self.__artifact:
            tmp_proj = self.__artifact["project"]
            if "id" in tmp_proj:
                self.__project_id = tmp_proj["id"]
            else:
                return False
        else:
            return False
        self.__valid = True
        return True

    def __extract_tracker(self):
        """
        Search for and extract the artifact tracker ID.

        :return: Extraction status. true if successful.
        :rtype: boolean
        """
        self.__valid = False
        if "tracker" in self.__artifact:
            tmp_track = self.__artifact["tracker"]
            if "id" in tmp_track:
                self.__tracker_id = tmp_track["id"]
            else:
                return False
        else:
            return False
        self.__valid = True
        return True

    def __extract_values(self):
        """
        Extract the list of values contained in the artifact. The values are converted to a string representation
        and added to a values list.
        """

        self.__reset_list(self.__values)
        self.__valid = False
        if "values" in self.__artifact:
            val_list = self.__artifact["values"]
            for val_item in val_list:
                # Convert the current value item to string
                val_parsed = ValueParser(val_item)
                if val_parsed.is_valid():
                    # if the current value item is the list of links extract all the required links!
                    if val_parsed.is_links():
                        self.__extract_links(val_item)
                    else:
                        # if this is an ordinary value item just store the item parameters
                        tmp_dict = {'id': val_parsed.get_id(),
                                    'label': val_parsed.get_label(),
                                    'value': val_parsed.get_value()}
                        self.__values.append(tmp_dict)
        self.__valid = True

    def __extract_links(self, item):
        """
        Search for and extract the artifact links. These can be either forward or reverse links (current artifact
        linking to a following artifact or a second artifact linking to the current artifact).
        Which links to extract is defined by the tracker chain setting. Only artifacts that are assigned to the
        required tracker are listed.
        """
        self.__reset_list(self.__links)
        self.__reset_list(self.__reverse_links)

        # Extract forward links, if any.
        if (self.__link_following == LinkFollowing.Forward) or (self.__link_following == LinkFollowing.All):
            if "links" in item:
                for lnk_tmp in item["links"]:
                    id_tmp = -1
                    trck_id_tmp = -1
                    # Extract the artifact ID
                    if "id" in lnk_tmp:
                        id_tmp = lnk_tmp["id"]
                    else:
                        continue
                    # Extract the tracker ID of the linked artifact
                    if "tracker" in lnk_tmp:
                        if "id" in lnk_tmp["tracker"]:
                            trck_id_tmp = lnk_tmp["tracker"]["id"]
                            # Append only the artifacts that belong to the correct tracker (next tracker in the chain)!
                            if trck_id_tmp == self.__child_id:
                                self.__links.append(id_tmp)

        # Extract reverse links, if any.
        if (self.__link_following == LinkFollowing.Reverse) or (self.__link_following == LinkFollowing.All):
            if "reverse_links" in item:
                for lnk_tmp in item["reverse_links"]:
                    id_tmp = -1
                    trck_id_tmp = -1
                    # Extract the artifact ID
                    if "id" in lnk_tmp:
                        id_tmp = lnk_tmp["id"]
                    else:
                        continue
                    # Extract the tracker ID of the linked artifact
                    if "tracker" in lnk_tmp:
                        if "id" in lnk_tmp["tracker"]:
                            trck_id_tmp = lnk_tmp["tracker"]["id"]
                            # Append only the artifacts that belong to the correct tracker (next tracker in the chain)!
                            if trck_id_tmp == self.__child_id:
                                self.__reverse_links.append(id_tmp)

    def __reset_list(self, items):
        """
        Clear list with python2.7 compatibility

        :type items: list
        """
        if at_least_python_3():
            items.clear()
        else:
            del items[:]
