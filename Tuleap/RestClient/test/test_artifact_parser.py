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

    def test_artifact_parser_get_links(self):
        links = [101, 102]
        self.assertEqual(self.artifact.get_links(), links)

    def test_artifact_parser_get_reverse_links(self):
        reverse_links = [21]
        self.assertEqual(self.artifact.get_reverse_links(), reverse_links)

    def test_artifact_parser_name(self):
        self.assertEqual(self.artifact.get_name(), "bugs #42")


if __name__ == '__main__':
    unittest.main()
