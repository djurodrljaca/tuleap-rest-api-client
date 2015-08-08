# REST API client for Tuleap open ALM

The purpose of this project is to create a python module that can be used for accessing a Tuleap instance using its REST API.

## Usage example:
```python
from Tuleap.RestClient.Client import Client

(success, errorInfo) = client.Login("https://tuleap.example.com:443/api",
                                    "username",
                                    "password") 

if success:
    (success, errorInfo, projectInfoList) = client.GetProjectList()

# TODO: add other examples when more API is implemented
    
client.Logout()
```