import json
import unittest

from Tuleap.RestClient.ArtifactParser import ArtifactParser


class ArtifactParserTest2(unittest.TestCase):
    def setUp(self):
        request_file = open("artifact_response_crossrefs.txt", "r")
        response = request_file.read()
        request_file.close()
        self.artifact = ArtifactParser(json.loads(response))

    def test_artifact_parser_name(self):
        self.assertEqual(self.artifact.get_name(), "story #26808")

    def test_git_ref(self):
        self.assertEqual([], self.artifact.get_out_git_references())

        self.assertEqual(self.artifact.get_in_git_references(),
                         ["git #tuleap/stable/8e6896fa659ad7bea33a042fe3d5e0c395c10dc8",
                          "git #tuleap/stable/8cc1b6d8251e4b4d77e8ff128ab41f15ff3c022e",
                          "git #tuleap/stable/7bb5667ecd29fc16c6ce92710632975c553e5857"])

    def test_artifact_links(self):
        self.assertEqual(self.artifact.get_links(), [])
        self.assertEqual(self.artifact.get_reverse_links(), [25714, 26754])

    def test_artifact_parser_links_types(self):
        self.assertEqual(self.artifact.get_links_types(), [])

        self.assertEqual(self.artifact.get_reverse_links_types(), [None, "_is_child"])


if __name__ == '__main__':
    unittest.main()
