"""
Created on 26.05.2017

:author: Humbert Moreaux

Tuleap REST API Client for Python
Copyright (c) Humbert Moreaux, All rights reserved.

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


class Git(object):
    """
    Handles "/git" methods of the Tuleap REST API.
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

    def request_repository(self, repository_id):
        """
        Request repository data from the server using the "/git" method of the Tuleap REST API.
        :param int repository_id: Git Repository ID
        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get repository
        relative_url = "/git/{:}".format(repository_id)
        success = self._connection.call_get_method(relative_url)

        # Parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success
