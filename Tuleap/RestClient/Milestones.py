import json

from Tuleap.RestClient.Commons import FieldsToFetch, FieldValuesFormat

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

    def get_last_response_message(self):
        """
        Get last response message.

        :return: Last response message
        :rtype: requests.Response

        :note: This is just a proxy to the connection's method.
        """
        self._connection.get_last_response_message()
