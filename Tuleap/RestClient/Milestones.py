"""
Created on 26.05.2017

:author: Moreaux Humbert

Tuleap REST API Client for Python
Copyright (c) Moreaux Humbert, All rights reserved.

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
from Tuleap.RestClient.Commons import Order


# Public -------------------------------------------------------------------------------------------


class Milestones(object):
    """
    Handles "/milestones" methods of the Tuleap REST API.

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

    def request_milestone(self, milestone_id):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get milestone
        relative_url = "/milestones/{:}".format(milestone_id)
        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_backlog(self, milestone_id, limit=10, offset=None):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID
        :param int limit: Optional parameter for maximum limit of returned changesets
        :param int offset: Optional parameter for start index for returned changesets

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get backlog
        relative_url = "/milestones/{:}/backlog".format(milestone_id)
        parameters = dict()

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

    def request_burndown(self, milestone_id):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get burndown data
        relative_url = "/milestones/{:}/burndown".format(milestone_id)
        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_cardwall(self, milestone_id):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get a cardwall
        relative_url = "/milestones/{:}/cardwall".format(milestone_id)
        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_content(self, milestone_id, limit=10, offset=None):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID
        :param int limit: Optional parameter for maximum limit of returned changesets
        :param int offset: Optional parameter for start index for returned changesets

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get content
        relative_url = "/milestones/{:}/content".format(milestone_id)
        parameters = dict()

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

    def request_sub_milestones(self, milestone_id,
                               fields=None,
                               query=None,
                               limit=10,
                               offset=None,
                               order=Order.Ascending):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID
        :param string fields: all/slim, Set of fields to return in the result
        :param int query: JSON object of search criteria properties
        :param int limit: Optional parameter for maximum limit of returned changesets
        :param int offset: Optional parameter for start index for returned changesets
        :param Order order: Ascending or descending order

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get sub-milestones
        relative_url = "/milestones/{:}/milestones".format(milestone_id)
        parameters = dict()

        if fields is not None:
            parameters["fields"] = fields

        if query is not None:
            parameters["query"] = query

        if limit is not None:
            parameters["limit"] = limit

        if offset is not None:
            parameters["offset"] = offset

        if order == Order.Descending:
            parameters["order"] = "desc"
        else:
            parameters["order"] = "asc"

        success = self._connection.call_get_method(relative_url, parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)
            self._count = self._connection.get_last_response_message().headers.get("X-PAGINATION-SIZE")
            self._pagination = self._connection.get_last_response_message().headers.get("X-PAGINATION-LIMIT-MAX", 10)

        return success

    def get_last_response_message(self):
        """
        Get last response message.

        :return: Last response message
        :rtype: requests.Response

        :note: This is just a proxy to the connection's method.
        """
        return self._connection.get_last_response_message()
