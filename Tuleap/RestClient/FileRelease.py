"""
Created on 02.05.2019

:author: Mathieu Auvray

Tuleap REST API Client for Python
Copyright (c) Mathieu Auvray, All rights reserved.

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


class FileRelease(object):
    """
    Handles "/frs_xxx" methods of the Tuleap REST API.

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

    def create_package(self, project_id, package_label):
        """
        Create a new package to the server using the "/frs_packages" method of the Tuleap REST
        API.

        :param int project_id: Project ID to store the package
        :param str package_label: Package label

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Create Package
        relative_url = "/frs_packages"

        if project_id and package_label :
            parameters = {
                "project_id": project_id,
                "label": package_label,
            }
        else:
            raise Exception("Error: invalid content values")

        success = self._connection.call_post_method(relative_url, data=parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def get_package(self, package_id):
        """
        Get a package from server using the "/frs_packages/{id}" method of the Tuleap REST
        API.

        :param int package_id: Packages ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get package
        relative_url = "/frs_packages/{:}".format(package_id)

        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def get_releases(self, package_id):
        """
        Get release of a package on server using the "/frs_packages/{id}/frs_release" method of the Tuleap REST
        API.

        :param int package_id: Packages ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get release
        relative_url = "/frs_packages/{:}/frs_release".format(package_id)

        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def create_release(self, package_id, release_name, release_note="", changelog="", status="active"):
        """
        Create a new release to the server using the "/frs_release" method of the Tuleap REST
        API.

        :param int package_id: Package ID
        :param str release_name: Release Name
        :param str release_note: Release note information
        :param str changelog : Change Log data
        :param str status of the release : 

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Create Release
        relative_url = "/frs_release"

        if package_id and release_name :
            parameters = {
                "package_id": package_id,
                "name": release_name,
                "release_note": release_note,
                "changelog": changelog,
                "status": status,
            }
        else:
            raise Exception("Error: invalid content values")

        success = self._connection.call_post_method(relative_url, data=parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def get_release(self, release_id):
        """
        Get a release from server using the "/frs_release/{id}" method of the Tuleap REST
        API.

        :param int release_id: Release ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get release
        relative_url = "/frs_release/{:}".format(release_id)

        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def get_files(self, release_id):
        """
        Get files of a release on server using the "/frs_release/{id}/files" method of the Tuleap REST
        API.

        :param int release_id: Release ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get files
        relative_url = "/frs_release/{:}/files".format(release_id)

        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def create_file(self, release_id, file_name, file_size):
        """
        Create a new file to the server using the "/frs_files" method of the Tuleap REST
        API.

        :param int release_id: release ID
        :param str file_name: file Name
        :param int file_size: size of the file to upload

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Create File
        relative_url = "/frs_files"

        if release_id and file_name and file_size:
            parameters = {
                "release_id": release_id,
                "name": file_name,
                "file_size": file_size,
            }
        else:
            raise Exception("Error: invalid content values")

        success = self._connection.call_post_method(relative_url, data=parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def get_file(self, file_id):
        """
        Get a file on server using the "/frs_files/{id}" method of the Tuleap REST
        API.

        :param int file_id: File ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get file
        relative_url = "/frs_files/{:}".format(file_id)

        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def delete_file(self, file_id):
        """
        Delete a file on server using the "/frs_files/{id}" method of the Tuleap REST
        API.

        :param int file_id: File ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Remove file
        relative_url = "/frs_files/{:}".format(file_id)

        success = self._connection.call_delete_method(relative_url)

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
