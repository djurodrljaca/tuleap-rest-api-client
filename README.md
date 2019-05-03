# REST API client for Tuleap open ALM

The purpose of this project is to create a python module that can be used for accessing a Tuleap
instance using its REST API.

## Usage example:
```python
from Tuleap.RestClient.Connection import Connection, CertificateVerification
from Tuleap.RestClient.Projects import Projects
from Tuleap.RestClient.Trackers import Tracker, FieldValues

connection = Connection()
success = connection.set_access_key("https://tuleap.example.com/api",
                                    "this-is-my-access-key")


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

## Upload example:
```python
from Tuleap.RestClient.Connection import Connection, CertificateVerification
from Tuleap.RestClient.FileRelease import FileRelease
from tusclient import client
from tusclient.client import TusClient
import os

tuleapURL = "https://tuleap.example.com"
userKey = "this-is-a-user-key"
filePath = "/directory/filepath.txt"
projectID = 123
packageName = "Package Name"
releaseName = "Release Name"
fileName = "File Name"

connection = Connection()
success = connection.set_access_key(tuleapURL+"/api",
                                    userKey)

if success:
    # Projects
    frs = FileRelease(connection)
    success = frs.create_package(projectID, packageName)
    if success:
        package = frs.get_data()
        success = frs.create_release(package['id'],releaseName)
        if success:
            release = frs.get_data()
            success = frs.create_file(release['id'], fileName, os.path.getsize(filePath))
            if success:
                file = frs.get_data()
                my_client = client.TusClient(tuleapURL+file['upload_href'],
                                             headers={'X-Auth-AccessKey':userKey})
                uploader = my_client.uploader(filePath, url=tuleapURL+file['upload_href'])
                uploader.upload()

connection.logout()
```

## Supported versions:

* 2.7
* 3.3
* 3.6
