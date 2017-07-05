import unittest
import json
from Tuleap.RestClient.ArtifactParser import ArtifactParser


class ArtifactParserTest(unittest.TestCase):
    def setUp(self):
        request_file = open("Tuleap/RestClient/test/request_artifact_response.txt", "r")
        response = request_file.read()
        request_file.close()
        self.artifact = ArtifactParser(json.loads(response))

    def test_artifact_parser_get_project_id(self):
        self.assertEqual(self.artifact.get_project_id(), 7)

    def test_artifact_parser_get_values(self):
        values = [{'id': 153, 'value': 'Display error on name field', 'type': 'TEXT', 'label': 'Summary'},
                  {'id': 142, 'value': '42', 'type': 'INTEGER', 'label': 'Artifact ID'}]
        self.assertEqual(self.artifact.get_values(), values)
