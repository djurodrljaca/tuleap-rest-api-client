"""
Created on 15.03.2016

:author: Andrej Nussdorfer

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

from Tuleap.RestClient.Commons import FieldValues

# Public -------------------------------------------------------------------------------------------


class Reports(object):
    """
    Handles "/tracker_reports" methods of the Tuleap REST API.

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
        self._pagination = 10

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

    def request_report(self, report_id):
        """
        Request report definition from the server using the "/tracker_reports" method of the Tuleap REST
        API.

        :param int report_id: Report ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get tracker
        relative_url = "/tracker_reports/{:}".format(report_id)

        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_artifact_list(self,
                              report_id,
                              field_values=FieldValues.No,
                              limit=10,
                              offset=None):
        """
        Request list of report artifacts from the server using the "/tracker_reports/{id}/artifacts"
        method of the  REST API.

        :param int report_id: Report ID
        :param FieldValues field_values: Field values
        :param int limit: Optional parameter for maximum limit of returned artifacts
        :param int offset: Optional parameter for start index for returned artifacts

        :return: success: Success or failure
        :rtype: bool

        The query parameter has to be in one of these formats:

        - The basic form of a property is [field_id|field_shortname] : [number|string|array(number)]

          Example: {"1258" : "bug"} OR {"title" : "bug"}

        - The complex form of a property is "field_id" : {"operator" : "operator_name", "value" :
          [number|string|array(number)]}

          Example: {"title" : {"operator" : "contains", "value" : "bug"}}

        - For text or number-like fields, the allowed operators are ["contains"]. The value must be
          a string or number

        - For select-box-like fields, the allowed operators are ["contains"]. The value(s) are
          bind_value_id

        - For date-like fields, the allowed operators are ["="|"<"|">"|"between"]. Dates must be in
          ISO date format

          Full example: {"title" : "bug", "2458" : {"operator" : "between", "value", ["2014-02-25",
          "2014-03-25T00:00:00-05:00"]}}
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get artifact list
        relative_url = "/tracker_reports/{:}/artifacts".format(report_id)
        parameters = dict()

        if field_values == FieldValues.No:
            parameters["values"] = ""
        elif field_values == FieldValues.All:
            parameters["values"] = "all"
        else:
            raise Exception("Error: invalid field values")

        if limit is not None:
            parameters["limit"] = limit

        if offset is not None:
            parameters["offset"] = offset

        success = self._connection.call_get_method(relative_url, parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)
            self._count = self._connection.get_last_response_message().headers.get("X-PAGINATION-SIZE")
            self._pagination = self._connection.get_last_response_message().headers.get("X-PAGINATION-LIMIT-MAX", 10)

        return success

    def get_last_response_message(self):
        """
        Get last response message.

        :return: Last response message
        :rtype: requests.Response

        :note: This is just a proxy to the connection's method.
        """
        self._connection.get_last_response_message()
