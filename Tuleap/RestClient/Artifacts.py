"""
Created on 16.03.2016

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

import json

from Tuleap.RestClient.Commons import FieldsToFetch, FieldValuesFormat, FieldValuesStructure

# Public -------------------------------------------------------------------------------------------


class Artifacts(object):
    """
    Handles "/artifacts" methods of the Tuleap REST API.

    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _data: dict | list[dict]
    """

    def __init__(self, connection):
        """
        Constructor

        :param connection: connection object (must already be logged in)
        :type connection: Tuleap.RestClient.Connection.Connection
        """
        self._connection = connection
        self._data = None
        self._count = 0
        self._pagination = 10

    def get_connection(self):
        """
        Get data received in the last response message.

        :return: Response data
        :rtype: dict | list[dict]

        :note: One of the request method should be successfully executed before this method is
               called!
        """
        return self._connection

    def get_data(self):
        """
        Get data received in the last response message.

        :return: Response data
        :rtype: dict | list[dict]

        :note: One of the request method should be successfully executed before this method is
               called!
        """
        return self._data

    def get_count(self):
        """
        Get number of maximum items corresponding to the last response header.
        
        :return: Response count
        :rtype: int
        
        :note: One of the request method should be successfully executed before this method is
               called!
        """
        return int(self._count) if self._count is not None else None

    def get_pagination(self):
        """
        Get number of items limitation by request corresponding to the last response header.
        
        :return: Response pagination
        :rtype: int
        
        :note: One of the request method should be successfully executed before this method is
               called!
        """
        return int(self._pagination) if self._pagination is not None else None

    def request_artifact(self,
                         artifact_id,
                         values_format=FieldValuesFormat.All, tracker_structure_format=FieldValuesStructure.Minimal):
        """
        Request artifact data from the server using the "/artifacts" method of the Tuleap REST
        API.

        :param int artifact_id: Artifact ID
        :param FieldValuesFormat values_format: Format of the value fields

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get artifact
        relative_url = "/artifacts/{:}".format(artifact_id)
        parameters = dict()

        if not(values_format == FieldValuesFormat.No):
            if values_format == FieldValuesFormat.Collection:
                parameters["values_format"] = "collection"
            elif values_format == FieldValuesFormat.ByField:
                parameters["values_format"] = "by_field"
            elif values_format == FieldValuesFormat.All:
                parameters["values_format"] = "all"
            else:
                raise Exception("Error: invalid value formatting")

        if not(tracker_structure_format == FieldValuesStructure.Minimal):
            parameters["tracker_structure_format"] = "complete"
        else:
            parameters["tracker_structure_format"] = "minimal"
            
        success = self._connection.call_get_method(relative_url, parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_changeset(self,
                          artifact_id,
                          fields_to_fetch=FieldsToFetch.All,
                          limit=10,
                          offset=None):
        """
        Request list of artifact changesets from the server using the "/artifacts/{id}/changesets"
        method of the  REST API.

        :param int artifact_id: Artifact ID
        :param FieldsToFetch fields_to_fetch: Fields to fetch
        :param int limit: Optional parameter for maximum limit of returned changesets
        :param int offset: Optional parameter for start index for returned changesets

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get artifact list
        relative_url = "/artifacts/{:}/changesets".format(artifact_id)
        parameters = dict()

        if fields_to_fetch == FieldsToFetch.All:
            parameters["fields"] = "all"
        elif fields_to_fetch == FieldsToFetch.Comments:
            parameters["fields"] = "comments"
        else:
            raise Exception("Error: invalid fields to fetch")

        if limit is not None:
            parameters["limit"] = limit

        if offset is not None:
            parameters["offset"] = offset

        success = self._connection.call_get_method(relative_url, parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)
            self._count = self._connection.get_last_response_message().headers.get("X-PAGINATION-SIZE")
            self._pagination = self._connection.get_last_response_message().headers.get("X-PAGINATION-LIMIT-MAX", 10)

        return success

    def create_artifact(self,
                        tracker_id,
                        values_by_field=None, values=None):
        """
        Create an artifact in a tracker from the server using the "/artifacts" method of the  REST API.

        :param int tracker_id: Tracker ID
        :param values_by_field: Values by field ex: 
            { "title": {"value": "title"}, "remaining_effort": {"value": 75} }
        :param values: values ex:
            "values": [
                    {"field_id": 1806, "value" : "my new artifact"},
                    {"field_id": 1841, "bind_value_ids" : [254,598,148]}
                ]

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Create an artifact
        relative_url = "/artifacts"
        parameters = dict()

        if tracker_id:
            parameters["tracker"] = {"id": tracker_id}
        else:
            raise Exception("Error: invalid tracker_id value")

        if not values_by_field and not values:
            raise Exception("Error: invalid values_by_field or values, at least one of this field should be provided")
        elif values_by_field and values:
            raise Exception("Error: REST API refuse to use values_by_field and values in the same request. You must choose one method")

        if values_by_field:
            parameters["values_by_field"] = values_by_field
        
        if values:
            parameters["values"] = values

        success = self._connection.call_post_method(relative_url, data=parameters)
        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def create_artifact_from(self,
                        tracker_id, from_artifact_id
                        ):
        """
        Create an artifact from another artifact in a tracker using the "/artifacts" method of the  REST API.

        :param int tracker_id: Tracker ID where the artifact will be created
        :param int from_artifact_id: Id of the artifact to copy

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Create an artifact
        relative_url = "/artifacts"
        parameters = dict()

        if tracker_id:
            parameters["tracker"] = {"id": tracker_id}
        else:
            raise Exception("Error: invalid tracker_id value")

        if from_artifact_id:
            parameters["from_artifact"] = {"id": from_artifact_id}
        else:
            raise Exception("Error: invalid from_artifact_id value")

        success = self._connection.call_post_method(relative_url, data=parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def update_artifact(self, artifact_id, values):
        """
        Update an artifact with some values using the "/artifacts/<artifact_id>" method PUT of the  REST API.

        :param int artifact_id: Artifact ID of the artifact to update
        :param list values: Values is a list of differents fields to update ex: 
            [{"field_id": xxxx, "type": "art_link", "label": "Links", "links": [{"id": xxxx, "uri": "artifacts/xxxx"}]}]

        :return: success: Success or failure
        :rtype: bool
        """
         # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Create an artifact
        relative_url = "/artifacts/" + str(artifact_id)
        parameters = dict()

        if values and isinstance(values, list):
            parameters["values"] = values
        else:
            raise Exception("Error: invalid values value")

        success = self._connection.call_put_method(relative_url, data=parameters)
        # parse response
        if success:
            self._data = self._connection.get_last_response_message().text

        return success

    def get_last_response_message(self):
        """
        Get last response message.

        :return: Last response message
        :rtype: requests.Response

        :note: This is just a proxy to the connection's method.
        """
        return self._connection.get_last_response_message()
