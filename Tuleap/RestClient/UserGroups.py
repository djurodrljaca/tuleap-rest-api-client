"""
Created on 02.09.2025

:author: SALVATOR Valentin

Tuleap REST API Client for Python
Copyright (c) Salvator Valentin, All rights reserved.

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

class UserGroups(object):
    """
    Handles "/user_groups" methods of the Tuleap REST API.

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

    def request_user_group(self, user_group_id):
        """
        Request user group data from the server using the "/user_groups/id" method of the Tuleap REST
        API.

        :param int user_group_id: User group ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get user
        relative_url = "/user_groups/{:}".format(user_group_id)


        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_users_in_group(self, user_group_id):
        """
        Request user group data from the server using the "/user_groups/id/users" method of the Tuleap REST
        API.

        :param int user_group_id: User group ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get user
        relative_url = "/user_groups/{:}/users".format(user_group_id)


        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def set_user_group_users(self, user_group_id, user_ids):
        """
        Set a group id with some values using the "/user_groups/id/users" method PUT of the  REST API.

        :param int group_id: User group ID to update
        :param [int] user_ids: Users to add to user_group
            {
                "user_references": [
                    {
                        "id": user_id1
                    },
                    {
                        "id": user_id2
                    }
                ]
            }

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        urd = [{"id": uid} for uid in user_ids]
        user_references_data = {'user_references': urd}

        # Create an artifact
        relative_url = "/user_groups/{:}/users".format(user_group_id)
        success = self._connection.call_put_method(relative_url, data=user_references_data)

        # parse response
        if success:
            self._data = self._connection.get_last_response_message().text

        return success

    def add_users_in_group(self, user_group_id, user_ids):
        """
        Update a group id with some values using the "/user_groups/id/users" method PUT of the  REST API.

        :param int group_id: User group ID to update
        :param [int] user_ids: Users to add to user_group

        :return: success: Success or failure
        :rtype: bool
        """

        if isinstance(user_ids, int):
            user_ids = [user_ids]

        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get current grp users
        success = self.request_users_in_group(user_group_id)
        if not success:
            return False

        prev_grp_users_json = self.get_data()
        new_grp_users = [item["id"] for item in prev_grp_users_json]

        for new_id in user_ids:
            if not new_id in new_grp_users:
                new_grp_users.append(new_id)

        success = self.set_user_group_users(user_group_id, new_grp_users)

        return success

    def remove_users_in_group(self, user_group_id, user_ids):
        """
        Update a group id with some values using the "/user_groups/id/users" method PUT of the  REST API.

        :param int group_id: User group ID to update
        :param [int] user_ids: Users to add to user_group

        :return: success: Success or failure
        :rtype: bool
        """

        if isinstance(user_ids, int):
            user_ids = [user_ids]

        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get current grp users
        success = self.request_users_in_group(user_group_id)
        if not success:
            return False

        prev_grp_users_json = self.get_data()
        new_grp_users = [item["id"] for item in prev_grp_users_json]

        for rem_id in user_ids:
            if rem_id in new_grp_users:
                new_grp_users.remove(rem_id)

        success = self.set_user_group_users(user_group_id, new_grp_users)

        return success

    def get_last_response_message(self):
        """
        Get last response message.

        :return: Last response message
        :rtype: requests.Response

        :note: This is just a proxy to the connection's method.
        """
        return self._connection.get_last_response_message()
