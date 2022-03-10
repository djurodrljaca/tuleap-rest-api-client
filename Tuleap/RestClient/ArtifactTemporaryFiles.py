"""
Created on 29.12.2021

:author: Guedon Nicolas

Tuleap REST API Client for Python
Copyright (c) Guedon Nicolas, All rights reserved.

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


class ArtifactTemporaryFiles(object):
    """
    Handles "/artifact_temporary_files" methods of the Tuleap REST API.

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
        self._pagination = 1048576
        self._quota = 0
        self._chuncksize = 0

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

    def get_chunk(self, file_id, limit=1048576, offset=None,):
        """
        Request artifact files chunk from the server using the "/artifact_temporary_files" method of the Tuleap REST
        API.
        
        :param int file_id: File ID
        :param int limit: Optional parameter for maximum limit of returned changesets
        :param int offset: Optional parameter for start index for returned changesets
        
        :return: success: Success or failure
        :rtype: bool
        """

        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get tracker
        relative_url = "/artifact_files/{:}".format(file_id)
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
            self._pagination = self._connection.get_last_response_message().headers.get("X-PAGINATION-LIMIT-MAX", limit)
            
        return success

    def get_files_representation(self, limit=10, offset=None):
        """
        Request temporary files representation from the server using the "/artifact_temporary_files" method of the Tuleap REST
        API.
        
        :param int limit: Optional parameter for maximum limit of returned changesets
        :param int offset: Optional parameter for start index for returned changesets
        
        :return: success: Success or failure
        :rtype: bool
        """

        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False
        
        # Get tracker
        relative_url = "/artifact_temporary_files"
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
            self._pagination = self._connection.get_last_response_message().headers.get("X-PAGINATION-LIMIT-MAX", limit)
            self._quota = self._connection.get_last_response_message().headers.get("x-quota")
            self._chunksize= self._connection.get_last_response_message().headers.get("x-upload-max-file-chunksize")
            
        return success

    def create_temporary_file(self, name, mimetype, content, description=""):
        """
        Create a temporary file on the server using the "/artifact_temporary_files" method of the  REST API.

        :param name: name of the file
        :param mimetype: mime type of the file
        :param content: chunck of the part
        :param description: description of the file
         
         ex: 
            { "name": "string", "mimetype": "string", "content": "string", "description": "string"}

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Create an artifact
        relative_url = "/artifact_temporary_files"
        parameters = dict()

        parameters["name"]        = name
        parameters["mimetype"]    = mimetype
        parameters["content"]     = content
        parameters["description"] = description

        success = self._connection.call_post_method(relative_url, data=parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def update_temporary_file(self, file_id, content, offset=None):
        """
        Update an existing temporary file by adding chunk on the server using the "/artifact_temporary_files" method of the  REST API.

        :param file_id: id of the file
        :param content: additional chunck of the file
        :param offset: number of the part to upload (2, 3, 4..)
         
         ex: 
            { "name": "string", "mimetype": "string", "content": "string", "description": "string"}

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Create an artifact
        relative_url = "/artifact_temporary_files/" + str(file_id)
        parameters = dict()

        parameters["content"] = content

        if offset is not None:
            parameters["offset"] = offset

        success = self._connection.call_put_method(relative_url, data=parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def delete_temporary_file(self, file_id):
        """
        Delete a temporary file on server using the "/artifact_temporary_files/{id}" method of the Tuleap REST
        API.

        :param int file_id: File ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Remove file
        relative_url = "/artifact_temporary_files/{:}".format(file_id)

        success = self._connection.call_delete_method(relative_url)

        # parse response
        if success:
            self._data = self._connection.get_last_response_message()

        return success

    def get_last_response_message(self):
        """
        Get last response message.

        :return: Last response message
        :rtype: requests.Response

        :note: This is just a proxy to the connection's method.
        """
        self._connection.get_last_response_message()
