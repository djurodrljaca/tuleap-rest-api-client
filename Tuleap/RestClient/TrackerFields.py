"""
Created on 07.12.2022

:author: Nicolas Guedon

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

# Public -------------------------------------------------------------------------------------------


class TrackerFields(object):
    """
    Handles "/tracker_fields" methods of the Tuleap REST API.
    
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

    def create_values(self, field_id, values):
        """
        Create new  alues on a field from the server using the "/racker_fields" method of the  REST API.

        :param int field_id: Field ID
        :param list values: values ex:
            ["my first new value", "my second new value"]

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Create the new value on the field
        relative_url = "/tracker_fields/{:}".format(field_id)
        parameters = dict()

        if values:
            parameters["new_values"] = values

        success = self._connection.call_patch_method(relative_url, data=parameters)
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