"""
Created on 08.08.2015

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


import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from Tuleap.RestClient.Commons import CertificateVerification
from Tuleap.RestClient.utils import at_least_python_3
if at_least_python_3():
    import urllib.parse
else:
    import urllib

# Public -------------------------------------------------------------------------------------------


class Connection(object):
    """
    Connection to the server.
    
    During login the REST API URL, authentication parameters and certificate verification options
    are supplied. After a successful login HTTP methods (DELETE, GET, POST) can be called
    and this class will prepare all the data needed to successfully call the method.
    
    The data that will be prepared is:
    * the full URL for the method (base URL combined with relative URL and additional parameters)
    * authentication parameters (authentication ID and token)
    * other options (certificate verification)
    
    Below are some examples of URL's mentioned above.
        
    Example without parameters:
    * base URL:     "https://tuleap.example.com:443/api"
    * relative URL: "/tokens"
    * full URL:     "https://tuleap.example.com:443/api/tokens"
    
    Example with single parameter:
    * base URL:     "https://tuleap.example.com:443/api"
    * relative URL: "/projects"
    * parameters:   {"limit": 10}
    * full URL:     "https://tuleap.example.com:443/api/projects?limit=10"
    
    Example with multiple parameters:
    * base URL:     "https://tuleap.example.com:443/api"
    * relative URL: "/projects"
    * parameters:   {"limit": 10, "offset": 50}
    * full URL:     "https://tuleap.example.com:443/api/projects?limit=10&offset=50"
    
    Fields type information:
    :type _isLoggedIn: bool
    :type _baseUrl: str
    :type _loginToken: _LoginToken
    :type _verifyCertificate: bool
    :type _authenticationHeaders: dict
    :type _lastResponseMessage: requests.Response
    """

    def __init__(self):
        """
        Constructor
        """
        self._isLoggedIn = False
        self._baseUrl = ""
        self._loginToken = _LoginToken()
        self._verifyCertificate = True
        self._authenticationHeaders = None
        self._lastResponseMessage = None

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self._clear()

    def is_logged_in(self):
        """
        Check if logged in
        
        :return: Success or failure
        :rtype: bool
        """
        return self._isLoggedIn

    def login(self,
              base_url,
              username,
              password,
              certificate_verification=CertificateVerification.Enabled):
        """
        Log in to the selected Tuleap instance
        
        :param str base_url: URL of the selected Tuleap instance
                            (example: https://tuleap.example.com:443/api)
        :param str username: User name
        :param str password: Password
        :param certificate_verification: Enable or disable certificate verification
        :type certificate_verification: CertificateVerification
        
        :return: Success or failure
        :rtype: bool
        """
        # Clear last response message
        self._lastResponseMessage = None
        
        # Log out if already logged in
        if self.is_logged_in():
            self.logout()
        
        # Get login token
        url = base_url + "/tokens"
        data = {"username": username, "password": password}
        verify_certificate = (certificate_verification == CertificateVerification.Enabled)
        
        response = requests.post(url, data=data, verify=verify_certificate)
        self._lastResponseMessage = response

        # parse response
        success = self._loginToken.parse(response)


        if success:
            # Save connection to the server
            self._baseUrl = base_url
            self._isLoggedIn = True
            self._verifyCertificate = verify_certificate
            self._authenticationHeaders = {"X-Auth-Token": self._loginToken.token,
                                           "X-Auth-UserId": str(self._loginToken.userId)}
            success = True
        
        return success

    def logout(self):
        """
        Log out of the connected Tuleap instance
        
        :return: success: Success or failure
        :rtype: bool
        """
        # Clear last response message
        self._lastResponseMessage = None
        
        # Check if logged in
        if not self.is_logged_in():
            # Not logged in
            return True
        
        # logout (delete login token)
        relative_url = "/tokens/{:}".format(self._loginToken.token)
        
        success = self.call_delete_method(relative_url)
        
        # Clean up after logout
        self._clear()
        
        return success

    def call_delete_method(self, relative_url, parameters=None, success_status_codes=list([200])):
        """
        Call DELETE method on the server
        
        :param str relative_url: relative part of URL
        :param dict parameters: parameters that should be added to the URL
        :param list[int] success_status_codes: list of HTTP status codes that represent 'success'
        
        :return: Success or failure
        :rtype: bool
        
        :note: Do not forget to add the leading '/' in the relative URL!
        """
        # Clear last response message
        self._lastResponseMessage = None
        
        # Check if logged in
        if not self.is_logged_in():
            return False
        
        # Check for leading '/' in the relative URL
        if not relative_url.startswith("/"):
            return False
        
        # Call the DELETE method
        success = False
        url = self._create_full_url(relative_url, parameters)
        
        response = requests.delete(url,
                                   headers=self._authenticationHeaders,
                                   verify=self._verifyCertificate)
        self._lastResponseMessage = response
        
        # Check for success
        if response.status_code in success_status_codes:
            success = True
        
        return success

    def call_get_method(self, relative_url, parameters=None, success_status_codes=list([200])):
        """
        Call GET method on the server
        
        :param str relative_url: relative part of URL
        :param dict parameters: parameters that should be added to the URL
        :param list[int] success_status_codes: list of HTTP status codes that represent 'success'
        
        :return: Success or failure
        :rtype: bool
        
        :note: Do not forget to add the leading '/' in the relative URL!
        """
        # Clear last response message
        self._lastResponseMessage = None
        
        # Check if logged in
        if not self.is_logged_in():
            return False
        
        # Check for leading '/' in the relative URL
        if not relative_url.startswith("/"):
            return False

        # Call the GET method
        success = False
        url = self._create_full_url(relative_url, parameters)
        
        response = requests.get(url,
                                headers=self._authenticationHeaders,
                                verify=self._verifyCertificate)
        self._lastResponseMessage = response
        
        # Check for success
        if response.status_code in success_status_codes:
            success = True
        
        return success

    def call_post_method(self, relative_url, data=None, success_status_codes=list([200, 201])):
        """
        Call POST method on the server
        
        :param str relative_url: relative part of URL
        :param dict data: request data
        :param list[int] success_status_codes: list of HTTP status codes that represent 'success'
        
        :return: Success or failure
        :rtype: bool
        
        :note: Do not forget to add the leading '/' in the relative URL!
        """
        # Clear last response message
        self._lastResponseMessage = None
        
        # Check if logged in
        if not self.is_logged_in():
            return False
        
        # Check for leading '/' in the relative URL
        if not relative_url.startswith("/"):
            return False
        
        # Call the POST method
        success = False
        url = self._create_full_url(relative_url)

        response = requests.post(url,
                                 json=data,
                                 headers=self._authenticationHeaders,
                                 verify=self._verifyCertificate)

        self._lastResponseMessage = response

        # Check for success
        if response.status_code in success_status_codes:
            success = True
        
        return success

    def get_last_response_message(self):
        """
        Get last response message
        
        :return: Last response message
        :rtype: requests.Response
        
        :note: This could be useful for diagnostic purposes when an error occurs
        """
        return self._lastResponseMessage

    def _create_full_url(self, relative_url, parameters=None):
        """
        Create "full" URL from a "relative" URL. "Full" URL is created by combining REST API URL
        with "relative" URL and optional parameters.
        
        :param str relative_url: relative part of URL
        :param dict parameters: parameters that should be appended to the URL
        
        :return: Full URL
        :rtype: str
        """
        url = self._baseUrl + relative_url
        
        if parameters is not None:
            if len(parameters) > 0:
                if at_least_python_3():
                    url = url + "?" + urllib.parse.urlencode(parameters)
                else:
                    url = url + "?" + urllib.urlencode(parameters)
        return url

    def _clear(self):
        """
        Clear all members
        """
        self._isLoggedIn = False
        self._baseUrl = ""
        self._loginToken = _LoginToken()
        self._verifyCertificate = True
        self._authenticationHeaders = None
        self._lastResponseMessage = None


# Private ------------------------------------------------------------------------------------------


class _LoginToken(object):
    """
    login token.
    
    Fields type information:
    :type userId: str
    :type token: str
    """

    def __init__(self):
        """
        Constructor
        """
        self.userId = ""
        self.token = ""

    def parse(self, response):
        """
        parse response object for login data
        
        :param requests.Response response: Response message from server
        
        :return: Success or failure
        :rtype: bool
        """
        success = False

        if response.status_code == 200 or response.status_code == 201:
            response_data = json.loads(response.text)
            
            # Save login token
            user_id = response_data["user_id"]
            token = response_data["token"]
            
            self.userId = user_id
            self.token = token
            success = True
        
        return success
