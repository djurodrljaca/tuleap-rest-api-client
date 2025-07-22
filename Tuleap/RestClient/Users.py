"""
Created on 29.12.2021

:author: Guedon Nicolas

Tuleap REST API Client for Python
Copyright (c) Guedon Nicolas, All rights reserved.

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

class Users(object):
    """
    Handles "/users" methods of the Tuleap REST API.
    
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

    def search_users(self, user_pattern, limit=10, offset=None):
        """
        Request project list from the server using the "/users" method of the Tuleap REST API.
        
        :param str pattern: At lest 3 char to launch a search on users
        :param int limit: Optional parameter for maximum limit of returned users
        :param int offset: Optional parameter for start index for returned users
        
        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get project list
        relative_url = "/users"
        parameters = dict()
        
        parameters["query"] = '{"shortname":"'+user_pattern+'"}'

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

    def request_user(self, user_id):
        """
        Request user data from the server using the "/users/id" method of the Tuleap REST
        API.

        :param int user_id: User ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get user
        relative_url = "/users/{:}".format(user_id)

        success = self._connection.call_get_method(relative_url)

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
        return self._connection.get_last_response_message()
