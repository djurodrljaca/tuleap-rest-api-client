'''
Created on 08.08.2015

@author: Djuro Drljaca
'''

import requests
import json

# Public classes -----------------------------------------------------------------------------------

class Client(object):
    '''
    Client for Tuleap open ALM REST API
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._connection = _Connection()
    
    def Login(self, apiUrl, username, password, verifyCertificate=True):
        '''
        Login to the selected Tuleap instance
        
        :param url: URL of the selected Tuleap instance
                    (example: https://tuleap.example.com:443/api)
        :type url: string
        
        :param username: User name
        :type username: string
        
        :param password: Password
        :type password: string
        
        :param verifyCertificate: Enable or disable certificate verification
        :type verifyCertificate: bool
        
        :return: Success or failure
        :rtype: bool
        '''
        # Logout if already logged in
        if self._connection.isLoggedIn:
            self.Logout()
        
        # Get login token
        url = apiUrl + "/tokens"
        parameters = {"username": username,
                      "password": password}
        
        response = requests.post(url, data=parameters, verify=verifyCertificate)
        
        # Parse response
        success = self._connection.loginToken.Parse(response)
        
        if success:
            # Save connection to the server
            self._connection.apiUrl = apiUrl
            self._connection.isLoggedIn = True
            self._connection.verifyCertificate = verifyCertificate
            self._connection.headers = {"X-Auth-Token": self._connection.loginToken.token,
                                        "X-Auth-UserId": self._connection.loginToken.userId}
            success = True
        
        return success
    
    def Logout(self):
        '''
        Logout of the connected Tuleap instance
        
        :return: Success or failure
        :rtype: bool
        '''
        # Logout (delete login token)
        relativeUrl = "tokens/{:}".format(self._connection.loginToken.token)
        url = self._connection.CreateFullUrl(relativeUrl)
        
        success = False
        response = requests.delete(url,
                                   headers=self._connection.headers,
                                   verify=self._connection.verifyCertificate)
        
        # Check if logout was successful
        if (response.status_code == 200):
            # Clean up after logout
            self._connection = _Connection()
            success = True
        
        return success

# Private classes ----------------------------------------------------------------------------------

class _Connection(object):
    '''
    Connection object holds the information regarding connection to the server
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.isLoggedIn = False
        self.apiUrl = ""
        self.loginToken = _LoginToken()
        self.verifyCertificate = True
        self.headers = None
    
    def CreateFullUrl(self, relativeUrl):
        '''
        Create "full" URL from a "relative" URL. "Full" URL is created by combining REST API URL
        with "relative" URL.
        
        Example:
        - REST API URL:   "https://tuleap.example.com:443/api"
        - "relative" URL: "tokens"
        - "full" URL:     "https://tuleap.example.com:443/api/tokens"
        
        :param relativeUrl: relative part of URL
        :type relativeUrl: string
        
        :return: Full URL
        :rtype: string
        '''
        url = self.apiUrl + "/" + relativeUrl
        
        return url

class _LoginToken(object):
    '''
    Login token
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.userId = ""
        self.token = ""
    
    def Parse(self, response):
        '''
        Parse response object for login data
        
        :param response: Response text from 
        :type response: json
        
        :return: Success or failure
        '''
        success = False
        
        if (response.status_code == 200):
            responseData = json.loads(response.text)
            
            # Save login token
            userId = responseData["user_id"]
            token = responseData["token"]
            
            self.userId = userId
            self.token = token
            success = True
        
        return success















        