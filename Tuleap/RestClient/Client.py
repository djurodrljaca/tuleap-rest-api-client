'''
Created on 08.08.2015

@author: Djuro Drljaca
'''

import requests
import json
import enum

# Public -------------------------------------------------------------------------------------------

class CertificateVerification(enum.Enum):
    '''
    Certificate verification
    '''
    Disabled = 0
    Enabled = 1

class ErrorInfo(object):
    '''
    Error information
    '''
    
    def __init__(self, response):
        '''
        Constructor
        
        :param response: Response message
        :type response: requests.Response
        '''
        self.errorCode = response.status_code
        self.responseText = response.text

class ProjectInfo(object):
    '''
    Project information
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self._rawData = None
    
    def GetId(self):
        '''
        Get Project ID
        
        :return: Project ID
        :rtype: int
        '''
        return self._rawData["id"]
    
    def GetUri(self):
        '''
        Get Project URI
        
        :return: Project URI
        :rtype: string
        '''
        return self._rawData["uri"]
    
    def GetLabel(self):
        '''
        Get Project label
        
        :return: Project label
        :rtype: string
        '''
        return self._rawData["label"]
    
    def GetShortName(self):
        '''
        Get Project short name
        
        :return: Project short name
        :rtype: string
        '''
        return self._rawData["shortname"]
    
    def GetResources(self):
        '''
        Get Project resources
        
        :return: Project resources
        :rtype: list[dict]
        '''
        return self._rawData["resources"]
    
    def GetAdditionalInformations(self):
        '''
        Get Project additional informations
        
        :return: Project additional informations
        :rtype: list
        '''
        return self._rawData["additional_informations"]
    
    @staticmethod
    def ParseList(response):
        '''
        Parse response object for project list
        
        :param response: Response message from server
        :type response: requests.Response
        
        :return: success: Success or failure, errorInfo: Error info, projectInfoList: Project list
        :rtype: (bool, ErrorInfo, list[ProjectInfo])
        '''
        success = False
        errorInfo = None
        projectInfoList = list()
        
        if (response.status_code == 200):
            responseData = json.loads(response.text)
            
            # Parse project list
            for item in responseData:
                projectInfo = ProjectInfo()
                projectInfo._rawData = item
                projectInfoList.append(projectInfo)
            
            success = True
        else:
            errorInfo = ErrorInfo(response)
        
        return (success, errorInfo, projectInfoList)

class Client(object):
    '''
    Client for Tuleap open ALM REST API
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._connection = _Connection()
    
    def Login(self,
              apiUrl,
              username,
              password,
              certificateVerification = CertificateVerification.Enabled):
        '''
        Login to the selected Tuleap instance
        
        :param url: URL of the selected Tuleap instance
                    (example: https://tuleap.example.com:443/api)
        :type url: string
        
        :param username: User name
        :type username: string
        
        :param password: Password
        :type password: string
        
        :param certificateVerification: Enable or disable certificate verification
        :type certificateVerification: CertificateVerification
        
        :return: success: Success or failure, errorInfo: Error info
        :rtype: (bool, ErrorInfo)
        '''
        # Logout if already logged in
        if self._connection.isLoggedIn:
            self.Logout()
        
        # Get login token
        url = apiUrl + "/tokens"
        parameters = {"username": username,
                      "password": password}
        verifyCertificate = (certificateVerification == CertificateVerification.Enabled)
        
        response = requests.post(url, data=parameters, verify=verifyCertificate)
        
        # Parse response
        (success, errorInfo) = self._connection.loginToken.Parse(response)
        
        if success:
            # Save connection to the server
            self._connection.apiUrl = apiUrl
            self._connection.isLoggedIn = True
            self._connection.verifyCertificate = verifyCertificate
            self._connection.headers = {"X-Auth-Token": self._connection.loginToken.token,
                                        "X-Auth-UserId": self._connection.loginToken.userId}
            success = True
        
        return (success, errorInfo)
    
    def Logout(self):
        '''
        Logout of the connected Tuleap instance
        
        :return: success: Success or failure, errorInfo: Error info
        :rtype: (bool, ErrorInfo)
        '''
        # Check if logged in
        if not self._connection.isLoggedIn:
            # Not logged in
            return (True, None)
        
        # Logout (delete login token)
        relativeUrl = "tokens/{:}".format(self._connection.loginToken.token)
        url = self._connection.CreateFullUrl(relativeUrl)
        
        response = requests.delete(url,
                                   headers=self._connection.headers,
                                   verify=self._connection.verifyCertificate)
        
        # Check if logout was successful
        success = False
        errorInfo = None
        
        if (response.status_code == 200):
            success = True
        else:
            errorInfo = ErrorInfo(response)
        
        # Clean up after logout
        self._connection = _Connection()
        
        return (success, errorInfo)
    
    def GetProjectList(self, limit = None, offset = None):
        '''
        Get project list
        
        :param limit: Optional parameter for maximum limit of returned projects 
        :type limit: int
        
        :param offset: Optional parameter for for start index for returned projects
        :type offset: int
        
        :return: success: Success or failure, errorInfo: Error info, projectInfoList: Project list
        :rtype: (bool, ErrorInfo, list[ProjectInfo])
        '''
        # Get project list
        relativeUrl = "projects"
        parameters = dict()
        
        if (limit != None):
            parameters["limit"] = limit
        
        if (offset != None):
            parameters["offset"] = offset
        
        url = self._connection.CreateFullUrl(relativeUrl, parameters)
        
        response = requests.get(url,
                                headers=self._connection.headers,
                                verify=self._connection.verifyCertificate)
        
        # Parse response
        success = False
        errorInfo = None
        projectInfoList = None
        
        if (response.status_code == 200):
            (success, errorInfo, projectInfoList) = ProjectInfo.ParseList(response)
        else:
            errorInfo = ErrorInfo(response)
        
        return (success, errorInfo, projectInfoList)

# Private ------------------------------------------------------------------------------------------

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
    
    def CreateFullUrl(self, relativeUrl, parameters = {}):
        '''
        Create "full" URL from a "relative" URL. "Full" URL is created by combining REST API URL
        with "relative" URL and optional parameters.
        
        :param relativeUrl: relative part of URL
        :type relativeUrl: string
        
        :param parameters: parameters that should be appended to the URL
        :type parameters: dict()
        
        :return: Full URL
        :rtype: string
        
        Example without parameters:
        - REST API URL:   "https://tuleap.example.com:443/api"
        - "relative" URL: "tokens"
        - "full" URL:     "https://tuleap.example.com:443/api/tokens"
        
        Example with single parameter:
        - REST API URL:   "https://tuleap.example.com:443/api"
        - "relative" URL: "projects"
        - parameters:      {"limit": 10}
        - "full" URL:     "https://tuleap.example.com:443/api/projects?limit=10"
        
        Example with multiple parameters:
        - REST API URL:   "https://tuleap.example.com:443/api"
        - "relative" URL: "projects"
        - parameters:      {"limit": 10, "offset": 10}
        - "full" URL:     "https://tuleap.example.com:443/api/projects?limit=10&offest=10"
        '''
        url = self.apiUrl + "/" + relativeUrl
        
        if (len(parameters) > 0):
            parameterList = list(parameters.items())
            
            url = url + "?{:}={:}".format(parameterList[0][0], parameterList[0][1])
            
            for index in range(1, len(parameterList)):
                url = url + "&{:}={:}".format(parameterList[index][0], parameterList[index][1])
        
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
        
        :param response: Response message from server
        :type response: requests.Response
        
        :return: success: Success or failure, errorInfo: Error info
        :rtype: (bool, ErrorInfo)
        '''
        success = False
        errorInfo = None
        
        if (response.status_code == 200):
            responseData = json.loads(response.text)
            
            # Save login token
            userId = responseData["user_id"]
            token = responseData["token"]
            
            self.userId = userId
            self.token = token
            success = True
        else:
            errorInfo = ErrorInfo(response)
        
        return (success, errorInfo)















        