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
import Tuleap.RestClient.Filter as Filter

# Public -------------------------------------------------------------------------------------------

class Projects(object):
    '''
    Handles "Projects" part of the Tuleap REST API.
    
    Fields type information:
    :type _connection: Tuleap.RestClient.Connection.Connection
    :type _projectList: list[dict]
    '''
    
    def __init__(self, connection):
        '''
        Constructor
        
        :param Tuleap.RestClient.Connection.Connection connection: connection object (must already
                                                                   be logged in)
        '''
        self._connection = connection
        self._projectList = None
    
    def GetProjectList(self, filterQuery = None):
        '''
        Get project list.
        
        :param Filter.FilterQuery filterQuery: Used to filter the project list that was received
            from the server. To get the complete project list, set this parameter to "None".
        
        :return: Filtered project list
        :rtype: list[dict]
        
        :note: Project list should be requested from the server before this method is called!
        
        Filter parameters that can be used:
        * "id": project ID (int) 
        * "uri": project URI (str)
        * "label": project label (str)
        * "shortname": project short name (str)
        '''
        projectList = list()
        
        # Check if filtering is needed
        if (self._projectList != None):
            if (filterQuery != None):
                # Filter projects
                for project in self._projectList:
                    if filterQuery.Execute(project):
                        projectList.append(project)
            else:
                # Filter is not selected, return the complete project list
                projectList = self._projectList
        
        return projectList
    
    def RequestProjectList(self, limit = None, offset = None):
        '''
        Request project list from the server
        
        :param int limit: Optional parameter for maximum limit of returned projects
        :param int offset: Optional parameter for for start index for returned projects
        
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
            self._projectList = json.loads(self._connection.GetLastResponseMessage().text)
        
        return success
    
    def GetLastResponseMessage(self):
        '''
        Get last response message.
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This is just a proxy to the connection's method.
        '''
        self._connection.GetLastResponseMessage()





























