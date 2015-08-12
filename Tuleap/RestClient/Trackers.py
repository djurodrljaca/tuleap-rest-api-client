'''
Created on 12.08.2015

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

# Public -------------------------------------------------------------------------------------------

class Tracker(object):
    '''
    Handles "/trackers/{id}" method of the Tuleap REST API.
    
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
        Get tracker information object.
        
        :return: Tracker information
        :rtype: dict
        
        :note: Tracker information should be requested from the server before this method is called!
        '''
        return self._data
    
    def Request(self, trackerId):
        '''
        Request tracker information from the server
        
        :param int trackerId: Tracker ID
        
        :return: success: Success or failure
        :rtype: bool
        '''
        # Check if we are logged in
        if not self._connection.IsLoggedIn():
            return False
        
        # Get tracker
        relativeUrl = "/trackers/{:}".format(trackerId)
        
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

























