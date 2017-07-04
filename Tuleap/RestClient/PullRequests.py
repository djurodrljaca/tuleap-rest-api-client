"""
Created on 04.07.2017

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

# Public -------------------------------------------------------------------------------------------


class PullRequests(object):
    """
    Handles "/pull_requests" methods of the Tuleap REST API.

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

    def request_pull_request(self, pull_request_id):
        """
        Request pull request data from the server using the "/pull_requests" method of the Tuleap REST
        API.

        :param int pull_request_id: Pull request ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get pull request
        relative_url = "/pull_requests/{:}".format(pull_request_id)

        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_comments(self, pull_request_id, limit=10, offset=None):
        """
        Request pull request comments using the "/pull_requests" method of the Tuleap REST API.

        :param pull_request_id: Pull request ID
        :param int limit: Optional parameter for maximum limit of returned projects
        :param int offset: Optional parameter for start index for returned projects

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get pull request comments
        relative_url = "/pull_requests/{:}/comments".format(pull_request_id)
        parameters = dict()

        if limit is not None:
            parameters["limit"] = limit

        if offset is not None:
            parameters["offset"] = offset

        success = self._connection.call_get_method(relative_url, parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_file_diff(self, pull_request_id, path):
        """
        Request pull request diff of a given file using the "/pull_requests" method of the Tuleap REST API.

        :param pull_request_id: Pull request ID
        :param path: File path

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get pull request diff of a given file
        relative_url = "/pull_requests/{:}/file_diff".format(pull_request_id)
        parameters = dict()

        parameters["path"] = path

        success = self._connection.call_get_method(relative_url, parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_files(self, pull_request_id):
        """
        Request pull request files using the "/pull_requests" method of the Tuleap REST API.

        :param pull_request_id: Pull request ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get pull request files
        relative_url = "/pull_requests/{:}/files".format(pull_request_id)

        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def create_pull_request(self, repository_id, branch_src, repository_dest_id, branch_dest):
        """
        Create a pull request from the server using the "/pull_requests" method of the  REST API.

        :param int repository_id: Repository ID
        :param string branch_src: Branch source name
        :param int repository_dest_id: Destination repository ID
        :param string branch_dest: Destination repository name

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Create a pull request
        relative_url = "/pull_requests"
        parameters = dict()

        if repository_id and branch_src and repository_dest_id and branch_dest:
            parameters["content"] = {
                "repository_id": repository_id,
                "branch_src": branch_src,
                "repository_dest_id": repository_dest_id,
                "branch_dest": branch_dest,
            }
        else:
            raise Exception("Error: invalid content values")

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
