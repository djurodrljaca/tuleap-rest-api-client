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

from Tuleap.RestClient.Commons import FieldsToFetch, FieldValuesFormat

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

    def get_data(self):
        """
        Get data received in the last response message.

        :return: Response data
        :rtype: dict | list[dict]

        :note: One of the request method should be successfully executed before this method is
               called!
        """
        return self._data

    def request_artifact(self,
                         artifact_id,
                         values_format=FieldValuesFormat.All):
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
            elif values_format == FieldValuesFormat.Collection:
                parameters["values_format"] = "by_field"
            elif values_format == FieldValuesFormat.All:
                parameters["values_format"] = "all"
            else:
                raise Exception("Error: invalid value formatting")

        success = self._connection.call_get_method(relative_url)

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

        return success

    def create_artifact(self,
                        tracker_id,
                        values_by_field):
        """
        Create an artifact in a tracker from the server using the "/artifacts" method of the  REST API.

        :param int tracker_id: Tracker ID
        :param ValuesByField values_by_field: Values by field ex: 
            { "title": {"value": "title"}, "remaining_effort": {"value": 75} }

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

        if values_by_field:
            parameters["values_by_field"] = values_by_field
        else:
            raise Exception("Error: invalid values_by_field value")

        success = self._connection.call_post_method(relative_url, parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def get_last_response_message(self):
        """
        Get last response message.

        :return: Last response message
        :rtype: requests.Response

        :note: This is just a proxy to the connection's method.
        """
        self._connection.get_last_response_message()
