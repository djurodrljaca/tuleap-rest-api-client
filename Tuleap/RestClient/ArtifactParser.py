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
    """

    def __init__(self, item):
        """
        Constructor

        :param item: the artifact item to ber parsed
        :type item: dict

        """
        self.__artifact = item
        self.__project_id = -1
        self.__tracker_id = -1
        self.__values = []
        self.__links = []
        self.__reverse_links = []
        
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
        success = self.__extract_project()
        
        # Extract the tracker ID
        if success:
            success = self.__extract_tracker()
            
        # Extract the artifact values
        if success:
            success = self.__extract_values()

        return success

    def __extract_project(self):
        """
        Search for and extract the artifact project ID.

        :return: Extraction status. true if successful.
        :rtype: boolean
        """
        if "project" in self.__artifact:
            tmp_proj = self.__artifact["project"]
            if "id" in tmp_proj:
                self.__project_id = tmp_proj["id"]
            else:
                return False
        else:
            return False
        return True

    def __extract_tracker(self):
        """
        Search for and extract the artifact tracker ID.

        :return: Extraction status. true if successful.
        :rtype: boolean
        """
        if "tracker" in self.__artifact:
            tmp_track = self.__artifact["tracker"]
            if "id" in tmp_track:
                self.__tracker_id = tmp_track["id"]
            else:
                return False
        else:
            return False
        return True

    def __extract_values(self):
        """
        Extract the list of values contained in the artifact. The values are converted to a string
        representation and added to a values list.
        """
        if "values" in self.__artifact:
            for value_item in self.__artifact["values"]:
                # Convert the current value item to string
                value_parsed = ValueParser(value_item)
                if value_parsed.is_valid():
                    # if the current value item is the list of links extract all the required links!
                    if value_parsed.is_links():
                        self.__extract_links(value_item)
                    else:
                        # if this is an ordinary value item just store the item parameters
                        tmp_dict = {'id':    value_parsed.get_id(),
                                    'label': value_parsed.get_label(),
                                    'value': value_parsed.get_value(),
                                    'type':  value_parsed.get_type()}
                        self.__values.append(tmp_dict)
        return True

    def __extract_links(self, item):
        """
        Search for and extract the artifact links. These can be either forward or reverse links
        (current artifact linking to a following artifact or a second artifact linking to the
        current artifact).
        """
        # Extract forward links
        if "links" in item:
            for lnk_tmp in item["links"]:
                # Extract the artifact ID
                if "id" in lnk_tmp:
                    self.__links.append(lnk_tmp["id"])

        # Extract reverse links
        if "reverse_links" in item:
            for lnk_tmp in item["reverse_links"]:
                # Extract the artifact ID
                if "id" in lnk_tmp:
                    self.__reverse_links.append(lnk_tmp["id"])
