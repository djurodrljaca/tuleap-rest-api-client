'''
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
'''

import json
import enum

# Public -------------------------------------------------------------------------------------------

class Projects(object):
    '''
    Handles "/projects" method of the Tuleap REST API.
    
    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _data: list[dict]
    '''
    
    def __init__(self, connection):
        '''
        Constructor
        
        :param connection: connection object (must already be logged in)
        :type connection: Tuleap.RestClient.Connection.Connection
        '''
        self._connection = connection
        self._data = None
    
    def GetData(self, filterQuery = None):
        '''
        Get project list object.
        
        :param filterQuery: Used to filter the project list that was received from the server. To
                            get the complete project list, set this parameter to "None".
        :type filterQuery: Filter.FilterQuery
        
        :return: Filtered project list
        :rtype: list[dict]
        
        :note: Project list should be requested from the server before this method is called!
        
        Filter parameters that can be used:
        * "id": project ID (int) 
        * "uri": project URI (str)
        * "label": project label (str)
        * "shortname": project short name (str)
        '''
        # TODO: add sorting?
        
        projectList = list()
        
        # Check if filtering is needed
        if (self._data != None):
            if (filterQuery != None):
                # Filter projects
                for project in self._data:
                    if filterQuery.Execute(project):
                        projectList.append(project)
            else:
                # Filter is not selected, return the complete project list
                projectList = self._data
        
        return projectList
    
    def Request(self, limit = 10, offset = None):
        '''
        Request project list from the server
        
        :param int limit: Optional parameter for maximum limit of returned projects
        :param int offset: Optional parameter for start index for returned projects
        
        :return: success: Success or failure
        :rtype: bool
        '''
        # Check if we are logged in
        if not self._connection.IsLoggedIn():
            return False
        
        # Get project list
        relativeUrl = "/projects"
        parameters = dict()
        
        if (limit != None):
            parameters["limit"] = limit
        
        if (offset != None):
            parameters["offset"] = offset
        
        success = self._connection.CallGetMethod(relativeUrl, parameters)
        
        # Parse response
        if success:
            self._data = json.loads(self._connection.GetLastResponseMessage().text)
        
        return success
    
    def GetLastResponseMessage(self):
        '''
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        '''
        self._connection.GetLastResponseMessage()

class Project(object):
    '''
    Handles "/projects/{id}" method of the Tuleap REST API.
    
    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _data: dict
    '''
    
    def __init__(self, connection):
        '''
        Constructor
        
        :param connection: connection object (must already be logged in)
        :type connection: Tuleap.RestClient.Connection.Connection
        '''
        self._connection = connection
        self._data = None
    
    def GetData(self):
        '''
        Get project information object.
        
        :return: Project information
        :rtype: dict
        
        :note: Project information should be requested from the server before this method is called!
        '''
        return self._data
    
    def Request(self, projectId):
        '''
        Request project information from the server
        
        :param int projectId: Project ID
        
        :return: success: Success or failure
        :rtype: bool
        '''
        # Check if we are logged in
        if not self._connection.IsLoggedIn():
            return False
        
        # Get project
        relativeUrl = "/projects/{:}".format(projectId)
        
        success = self._connection.CallGetMethod(relativeUrl)
        
        # Parse response
        if success:
            self._data = json.loads(self._connection.GetLastResponseMessage().text)
        
        return success
    
    def GetLastResponseMessage(self):
        '''
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        '''
        self._connection.GetLastResponseMessage()

class Backlog(object):
    '''
    Handles "/projects/{id}/backlog" method of the Tuleap REST API.
    
    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _data: list[dict]
    '''
    
    def __init__(self, connection):
        '''
        Constructor
        
        :param connection: connection object (must already be logged in)
        :type connection: Tuleap.RestClient.Connection.Connection
        '''
        self._connection = connection
        self._data = None
    
    def GetData(self):
        '''
        Get backlog object.
        
        :return: Project backlog information
        :rtype: dict
        
        :note: Project backlog information should be requested from the server before this method is
               called!
        '''
        # TODO: add filtering?
        # TODO: add sorting?
        
        return self._data
    
    def Request(self, projectId, limit = 10, offset = None):
        '''
        Request project backlog information from the server
        
        :param int projectId: Project ID
        :param int limit: Optional parameter for maximum limit of returned backlog items
        :param int offset: Optional parameter for start index for returned backlog items
        
        :return: success: Success or failure
        :rtype: bool
        '''
        # Check if we are logged in
        if not self._connection.IsLoggedIn():
            return False
        
        # Get project
        relativeUrl = "/projects/{:}/backlog".format(projectId)
        parameters = dict()
        
        if (limit != None):
            parameters["limit"] = limit
        
        if (offset != None):
            parameters["offset"] = offset
        
        success = self._connection.CallGetMethod(relativeUrl, parameters)
        
        # Parse response
        if success:
            self._data = json.loads(self._connection.GetLastResponseMessage().text)
        
        return success
    
    # TODO: implement ordering of backlog items?
    # TODO: implement re-ordering (also adding?) of backlog items?
    
    def GetLastResponseMessage(self):
        '''
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        '''
        self._connection.GetLastResponseMessage()

class GitFields(enum.Enum):
    Basic = 0
    All = 1

class Git(object):
    '''
    Handles "/projects/{id}/git" method of the Tuleap REST API.
    
    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _data: dict
    '''
    
    def __init__(self, connection):
        '''
        Constructor
        
        :param connection: connection object (must already be logged in)
        :type connection: Tuleap.RestClient.Connection.Connection
        '''
        self._connection = connection
        self._data = None
    
    def GetData(self):
        '''
        Get git object.
        
        :return: Project git information
        :rtype: dict
        
        :note: Project git information should be requested from the server before this method is
               called!
        '''
        # TODO: add filtering?
        # TODO: add sorting?
        
        return self._data
    
    def Request(self, projectId, fields, limit = 10, offset = None):
        '''
        Request project git information from the server
        
        :param int projectId: Project ID
        :param GitFields fields: Basic or all fields
        :param int limit: Optional parameter for maximum limit of returned git items
        :param int offset: Optional parameter for start index for returned git items
        
        :return: success: Success or failure
        :rtype: bool
        '''
        # Check if we are logged in
        if not self._connection.IsLoggedIn():
            return False
        
        # Get project
        relativeUrl = "/projects/{:}/git".format(projectId)
        parameters = dict()
        
        if (fields == GitFields.Basic):
            parameters["fields"] = "basic"
        elif (fields == GitFields.All):
            parameters["fields"] = "all"
        else:
            raise Exception("Error: invalid git fields")
        
        if (limit != None):
            parameters["limit"] = limit
        
        if (offset != None):
            parameters["offset"] = offset
        
        success = self._connection.CallGetMethod(relativeUrl, parameters)
        
        # Parse response
        if success:
            self._data = json.loads(self._connection.GetLastResponseMessage().text)
        
        return success
    
    def GetLastResponseMessage(self):
        '''
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        '''
        self._connection.GetLastResponseMessage()

class Order(enum.Enum):
    Ascending = 0
    Descending = 1

class Milestones(object):
    '''
    Handles "/projects/{id}/milestones" method of the Tuleap REST API.
    
    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _data: list[dict]
    '''
    
    def __init__(self, connection):
        '''
        Constructor
        
        :param connection: connection object (must already be logged in)
        :type connection: Tuleap.RestClient.Connection.Connection
        '''
        self._connection = connection
        self._data = None
    
    def GetData(self):
        '''
        Get milestones object.
        
        :return: Project milestones information
        :rtype: dict
        
        :note: Project milestones information should be requested from the server before this method
               is called!
        '''
        # TODO: add sorting?
        # TODO: add filtering?
        
        return self._data
    
    def Request(self, projectId, order, limit = 10, offset = None):
        '''
        Request project milestones information from the server
        
        :param int projectId: Project ID
        :param Order order: Ascending or descending order
        :param int limit: Optional parameter for maximum limit of returned milestone items
        :param int offset: Optional parameter for start index for returned milestone items
        
        :return: success: Success or failure
        :rtype: bool
        '''
        # Check if we are logged in
        if not self._connection.IsLoggedIn():
            return False
        
        # Get project
        relativeUrl = "/projects/{:}/milestones".format(projectId)
        parameters = dict()
        
        if (order == GitFields.Basic):
            parameters["order"] = "basic"
        elif (order == GitFields.All):
            parameters["order"] = "all"
        else:
            raise Exception("Error: invalid order")
        
        if (limit != None):
            parameters["limit"] = limit
        
        if (offset != None):
            parameters["offset"] = offset
        
        success = self._connection.CallGetMethod(relativeUrl, parameters)
        
        # Parse response
        if success:
            self._data = json.loads(self._connection.GetLastResponseMessage().text)
        
        return success
    
    def GetLastResponseMessage(self):
        '''
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        '''
        self._connection.GetLastResponseMessage()

class PhpWiki(object):
    '''
    Handles "/projects/{id}/phpwiki" method of the Tuleap REST API.
    
    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _data: list[dict]
    '''
    
    def __init__(self, connection):
        '''
        Constructor
        
        :param connection: connection object (must already be logged in)
        :type connection: Tuleap.RestClient.Connection.Connection
        '''
        self._connection = connection
        self._data = None
    
    def GetData(self):
        '''
        Get PhpWiki object.
        
        :return: Project PhpWiki information
        :rtype: dict
        
        :note: Project PhpWiki information should be requested from the server before this method is
               called!
        '''
        # TODO: add filtering?
        # TODO: add sorting?
        
        return self._data
    
    def Request(self, projectId, limit = 10, offset = None, pageName = None):
        '''
        Request project PhpWiki information from the server
        
        :param int projectId: Project ID
        :param int limit: Optional parameter for maximum limit of returned PhpWiki items
        :param int offset: Optional parameter for start index for returned PhpWiki items
        :param str pageName: Optional parameter for part of the page name or the full page name to
                             search
        
        :return: success: Success or failure
        :rtype: bool
        '''
        # Check if we are logged in
        if not self._connection.IsLoggedIn():
            return False
        
        # Get project
        relativeUrl = "/projects/{:}/phpwiki".format(projectId)
        parameters = dict()
        
        if (limit != None):
            parameters["limit"] = limit
        
        if (offset != None):
            parameters["offset"] = offset
        
        if (pageName != None):
            parameters["pagename"] = pageName
        
        success = self._connection.CallGetMethod(relativeUrl, parameters)
        
        # Parse response
        if success:
            self._data = json.loads(self._connection.GetLastResponseMessage().text)
        
        return success
    
    def GetLastResponseMessage(self):
        '''
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        '''
        self._connection.GetLastResponseMessage()

class Plannings(object):
    '''
    Handles "/projects/{id}/plannings" method of the Tuleap REST API.
    
    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _data: list[dict]
    '''
    
    def __init__(self, connection):
        '''
        Constructor
        
        :param connection: connection object (must already be logged in)
        :type connection: Tuleap.RestClient.Connection.Connection
        '''
        self._connection = connection
        self._data = None
    
    def GetData(self):
        '''
        Get plannings object.
        
        :return: Project plannings information
        :rtype: dict
        
        :note: Project plannings information should be requested from the server before this method
               is called!
        '''
        # TODO: add filtering?
        # TODO: add sorting?
        
        return self._data
    
    def Request(self, projectId, limit = 10, offset = None):
        '''
        Request project plannings information from the server
        
        :param int projectId: Project ID
        :param int limit: Optional parameter for maximum limit of returned backlog items
        :param int offset: Optional parameter for start index for returned backlog items
        
        :return: success: Success or failure
        :rtype: bool
        '''
        # Check if we are logged in
        if not self._connection.IsLoggedIn():
            return False
        
        # Get project
        relativeUrl = "/projects/{:}/plannings".format(projectId)
        parameters = dict()
        
        if (limit != None):
            parameters["limit"] = limit
        
        if (offset != None):
            parameters["offset"] = offset
        
        success = self._connection.CallGetMethod(relativeUrl, parameters)
        
        # Parse response
        if success:
            self._data = json.loads(self._connection.GetLastResponseMessage().text)
        
        return success
    
    def GetLastResponseMessage(self):
        '''
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        '''
        self._connection.GetLastResponseMessage()

class Trackers(object):
    '''
    Handles "/projects/{id}/trackers" method of the Tuleap REST API.
    
    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _data: list[dict]
    '''
    
    def __init__(self, connection):
        '''
        Constructor
        
        :param connection: connection object (must already be logged in)
        :type connection: Tuleap.RestClient.Connection.Connection
        '''
        self._connection = connection
        self._data = None
    
    def GetData(self):
        '''
        Get trackers object.
        
        :return: Project trackers information
        :rtype: dict
        
        :note: Project trackers information should be requested from the server before this method
               is called!
        '''
        # TODO: add filtering?
        # TODO: add sorting?
        
        return self._data
    
    def Request(self, projectId, limit = 10, offset = None):
        '''
        Request project trackers information from the server
        
        :param int projectId: Project ID
        :param int limit: Optional parameter for maximum limit of returned backlog items
        :param int offset: Optional parameter for start index for returned backlog items
        
        :return: success: Success or failure
        :rtype: bool
        
        :warning: Response to this request will contain the complete configuration of each tracker
                  so it is advised to set a reasnoble "limit" value.
        '''
        # Check if we are logged in
        if not self._connection.IsLoggedIn():
            return False
        
        # Get project
        relativeUrl = "/projects/{:}/trackers".format(projectId)
        parameters = dict()
        
        if (limit != None):
            parameters["limit"] = limit
        
        if (offset != None):
            parameters["offset"] = offset
        
        success = self._connection.CallGetMethod(relativeUrl, parameters)
        
        # Parse response
        if success:
            self._data = json.loads(self._connection.GetLastResponseMessage().text)
        
        return success
    
    def GetLastResponseMessage(self):
        '''
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        '''
        self._connection.GetLastResponseMessage()

class UserGroups(object):
    '''
    Handles "/projects/{id}/user_groups" method of the Tuleap REST API.
    
    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _data: list[dict]
    '''
    
    def __init__(self, connection):
        '''
        Constructor
        
        :param connection: connection object (must already be logged in)
        :type connection: Tuleap.RestClient.Connection.Connection
        '''
        self._connection = connection
        self._data = None
    
    def GetData(self):
        '''
        Get user groups object.
        
        :return: Project user groups information
        :rtype: dict
        
        :note: Project user groups information should be requested from the server before this
               method is called!
        '''
        # TODO: add filtering?
        # TODO: add sorting?
        
        return self._data
    
    def Request(self, projectId, limit = 10, offset = None):
        '''
        Request project user groups information from the server
        
        :param int projectId: Project ID
        
        :return: success: Success or failure
        :rtype: bool
        '''
        # Check if we are logged in
        if not self._connection.IsLoggedIn():
            return False
        
        # Get project
        relativeUrl = "/projects/{:}/user_groups".format(projectId)
        parameters = dict()
        
        success = self._connection.CallGetMethod(relativeUrl, parameters)
        
        # Parse response
        if success:
            self._data = json.loads(self._connection.GetLastResponseMessage().text)
        
        return success
    
    def GetLastResponseMessage(self):
        '''
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        '''
        self._connection.GetLastResponseMessage()

























