import json
from Tuleap.RestClient.Commons import Order


# Public -------------------------------------------------------------------------------------------


class Milestones(object):
    """
    Handles "/milestones" methods of the Tuleap REST API.

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

    def request_milestone(self, milestone_id):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get milestone
        relative_url = "/milestones/{:}".format(milestone_id)
        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_backlog(self, milestone_id, limit=10, offset=None):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID
        :param int limit: Optional parameter for maximum limit of returned changesets
        :param int offset: Optional parameter for start index for returned changesets

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get backlog
        relative_url = "/milestones/{:}/backlog".format(milestone_id)
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

    def request_burndown(self, milestone_id):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get burndown data
        relative_url = "/milestones/{:}/burndown".format(milestone_id)
        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_cardwall(self, milestone_id):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get a cardwall
        relative_url = "/milestones/{:}/cardwall".format(milestone_id)
        success = self._connection.call_get_method(relative_url)

        # parse response
        if success:
            self._data = json.loads(self._connection.get_last_response_message().text)

        return success

    def request_content(self, milestone_id, limit=10, offset=None):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID
        :param int limit: Optional parameter for maximum limit of returned changesets
        :param int offset: Optional parameter for start index for returned changesets

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get content
        relative_url = "/milestones/{:}/content".format(milestone_id)
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

    def request_sub_milestones(self, milestone_id,
                               fields=None,
                               query=None,
                               limit=10,
                               offset=None,
                               order=Order.Ascending):
        """
        Request milestone data from the server using the "/milestones" method of the Tuleap REST API.

        :param int milestone_id: Milestone ID
        :param string fields: all/slim, Set of fields to return in the result
        :param int query: JSON object of search criteria properties
        :param int limit: Optional parameter for maximum limit of returned changesets
        :param int offset: Optional parameter for start index for returned changesets
        :param Order order: Ascending or descending order

        :return: success: Success or failure
        :rtype: bool
        """
        # Check if we are logged in
        if not self._connection.is_logged_in():
            return False

        # Get sub-milestones
        relative_url = "/milestones/{:}/milestones".format(milestone_id)
        parameters = dict()

        if fields is not None:
            parameters["fields"] = fields

        if query is not None:
            parameters["query"] = query

        if limit is not None:
            parameters["limit"] = limit

        if offset is not None:
            parameters["offset"] = offset

        if order == Order.Descending:
            parameters["order"] = "desc"
        else:
            parameters["order"] = "asc"

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
