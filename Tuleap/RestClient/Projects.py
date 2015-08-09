'''
Created on 09.08.2015

@author: Djuro Drljaca
'''

import json

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
    
    def GetProjectList(self, filter = None):
        '''
        Get project list.
        
        :param dict filter: Used to filter the project list that was received from the server. To
                            get the complete project list, set this parameter to "None".
        
        :return: Filtered project list
        :rtype: list[dict]
        
        :note: Project list should be requested from the server before this method is called!
        
        Filter parameters that can be used:
        * "id": project ID (int) 
        * "uri": project URI (string)
        * "label": project label (string)
        * "shortname": project short name (string)
        '''
        projectList = self._projectList
        
        # Check if filtering is needed
        if ((projectList != None) and (filter != None)):
            if (len(projectList) > 0):
                # Filter projects
                # TODO: implement
                # TODO: make a "Filter" module that takes a "list[dict]" object and a "Filter"
                #       object and filters the list?
                pass
        
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





























