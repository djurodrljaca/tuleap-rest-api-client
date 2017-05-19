import json


# Public -------------------------------------------------------------------------------------------


class BacklogItems(object):
    """
    Handles "/backlog_items" methods of the Tuleap REST API.

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

    def request_backlog_items(self, backlog_item_id, limit=10, offset=None):
        """
        Request backlog items from the server using the "/backlog_items" method of the Tuleap REST API.

        :param int backlog_item_id: Backlog Item ID
        :param int limit: Optional parameter for maximum limit of returned projects
        :param int offset: Optional parameter for start index for returned projects

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get backlog items
        relative_url = "/backlog_items/{:}".format(backlog_item_id)
        parameters = dict()

        if limit is not None:
            parameters["limit"] = limit

        if offset is not None:
            parameters["offset"] = offset

        success = self._connection.call_get_method(relative_url, parameters)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_children(self, backlog_item_id, limit=10, offset=None):
        """
        Request backlog item children from the server using the "/backlog_items" method of the Tuleap REST API.

        :param int backlog_item_id: Backlog Item ID
        :param int limit: Optional parameter for maximum limit of returned projects
        :param int offset: Optional parameter for start index for returned projects

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get children
        relative_url = "/backlog_items/{:}/children".format(backlog_item_id)
        parameters = dict()

        if limit is not None:
            parameters["limit"] = limit

        if offset is not None:
            parameters["offset"] = offset

        success = self._connection.call_get_method(relative_url, parameters)

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
