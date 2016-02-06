# REST API client for Tuleap open ALM

The purpose of this project is to create a python module that can be used for accessing a Tuleap
instance using its REST API.

## Usage example:
```python
from Tuleap.RestClient.Connection import Connection, CertificateVerification
from Tuleap.RestClient.Projects import Projects
from Tuleap.RestClient.Trackers import Tracker, FieldValues

connection = Connection()
success = connection.login("https://tuleap.example.com:443/api",
                           "username",
                           "password",
                           CertificateVerification.Disabled)

if success:
    # Projects
    projects = Projects(connection)
    success = projects.request_project_list()

    if success:
        project_list = projects.get_data()

    # Trackers
    tracker = Tracker(connection)
    success = tracker.request_artifact_list(tracker_id=20,
                                            field_values=FieldValues.All,
                                            limit=None)

    if success:
        artifact_list = tracker.get_data()

connection.logout()
```