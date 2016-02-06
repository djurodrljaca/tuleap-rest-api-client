"""
Created on 09.08.2015

:author: Djuro Drljaca

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
import enum


# Public -------------------------------------------------------------------------------------------


class GitFields(enum.Enum):
    Basic = 0
    All = 1


class Order(enum.Enum):
    Ascending = 0
    Descending = 1


class Projects(object):
    """
    Handles "/projects" methods of the Tuleap REST API.
    
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

    def request_project_list(self, limit=10, offset=None):
        """
        Request project list from the server using the "/projects" method of the Tuleap REST API.
        
        :param int limit: Optional parameter for maximum limit of returned projects
        :param int offset: Optional parameter for start index for returned projects
        
        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get project list
        relative_url = "/projects"
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

    def request_project(self, project_id):
        """
        Request project information from the server using the "/projects{id}" method of the Tuleap
        REST API.
        
        :param int project_id: Project ID
        
        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get project
        relative_url = "/projects/{:}".format(project_id)
        
        success = self._connection.call_get_method(relative_url)
        
        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)
        
        return success

    def request_backlog(self, project_id, limit=10, offset=None):
        """
        Request project backlog information from the server using the "/projects/{id}/backlog"
        method of the Tuleap REST API.
        
        :param int project_id: Project ID
        :param int limit: Optional parameter for maximum limit of returned backlog items
        :param int offset: Optional parameter for start index for returned backlog items
        
        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get project
        relative_url = "/projects/{:}/backlog".format(project_id)
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

    def request_git(self, project_id, fields, limit=10, offset=None):
        """
        Request project git information from the server using the "/projects/{id}/git" method of the
        Tuleap REST API.
        
        :param int project_id: Project ID
        :param GitFields fields: Basic or all fields
        :param int limit: Optional parameter for maximum limit of returned git items
        :param int offset: Optional parameter for start index for returned git items
        
        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get project
        relative_url = "/projects/{:}/git".format(project_id)
        parameters = dict()
        
        if fields == GitFields.Basic:
            parameters["fields"] = "basic"
        elif fields == GitFields.All:
            parameters["fields"] = "all"
        else:
            raise Exception("Error: invalid git fields")
        
        if limit is not None:
            parameters["limit"] = limit
        
        if offset is not None:
            parameters["offset"] = offset
        
        success = self._connection.call_get_method(relative_url, parameters)
        
        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)
        
        return success

    def request_milestones(self, project_id, order, limit=10, offset=None):
        """
        Request project milestones information from the server using the "/projects/{id}/milestones"
        method of the  REST API.
        
        :param int project_id: Project ID
        :param Order order: Ascending or descending order
        :param int limit: Optional parameter for maximum limit of returned milestones
        :param int offset: Optional parameter for start index for returned milestones
        
        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get project
        relative_url = "/projects/{:}/milestones".format(project_id)
        parameters = dict()
        
        if order == Order.Ascending:
            parameters["order"] = "asc"
        elif order == Order.Descending:
            parameters["order"] = "desc"
        else:
            raise Exception("Error: invalid order")
        
        if limit is not None:
            parameters["limit"] = limit
        
        if offset is not None:
            parameters["offset"] = offset
        
        success = self._connection.call_get_method(relative_url, parameters)
        
        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)
        
        return success

    def request_php_wiki(self, project_id, limit=10, offset=None, page_name=None):
        """
        Request project PhpWiki information from the server using the "/projects/{id}/phpwiki"
        method of the  REST API.
        
        :param int project_id: Project ID
        :param int limit: Optional parameter for maximum limit of returned PhpWiki pages
        :param int offset: Optional parameter for start index for returned PhpWiki pages
        :param str page_name: Optional parameter for part of the page name or the full page name to
                              search
        
        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get project
        relative_url = "/projects/{:}/phpwiki".format(project_id)
        parameters = dict()
        
        if limit is not None:
            parameters["limit"] = limit
        
        if offset is not None:
            parameters["offset"] = offset
        
        if page_name is not None:
            parameters["pagename"] = page_name
        
        success = self._connection.call_get_method(relative_url, parameters)
        
        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)
        
        return success

    def request_plannings(self, project_id, limit=10, offset=None):
        """
        Request project plannings information from the server using the "/projects/{id}/plannings"
        method of the  REST API.
        
        :param int project_id: Project ID
        :param int limit: Optional parameter for maximum limit of returned planning items
        :param int offset: Optional parameter for start index for returned planning items
        
        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get project
        relative_url = "/projects/{:}/plannings".format(project_id)
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

    def request_trackers(self, project_id, limit=10, offset=None):
        """
        Request project trackers information from the server using the "/projects/{id}/trackers"
        method of the  REST API.
        
        :param int project_id: Project ID
        :param int limit: Optional parameter for maximum limit of returned trackers
        :param int offset: Optional parameter for start index for returned trackers
        
        :return: success: Success or failure
        :rtype: bool
        
        :warning: Response to this request will contain the complete configuration of each tracker
                  which could be very big, so it is advised to set a reasonable "limit" value.
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get project
        relative_url = "/projects/{:}/trackers".format(project_id)
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

    def request_user_groups(self, project_id, limit=10, offset=None):
        """
        Request project user groups information from the server using the
        "/projects/{id}/user_groups" method of the  REST API.
        
        :param int project_id: Project ID
        :param int limit: Optional parameter for maximum limit of returned user groups
        :param int offset: Optional parameter for start index for returned user groups
        
        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get project
        relative_url = "/projects/{:}/user_groups".format(project_id)
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

    def get_last_response_message(self):
        """
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        """
        self._connection.get_last_response_message()
