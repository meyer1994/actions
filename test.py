from unittest import TestCase

from main import GitHubAction


class TestAction(TestCase):
    def test_action(self):
        """ Generates a GitHub action """
        action = GitHubAction()

        data = action.dict()

        expected = {
            'name': 'build',
            'on': ['push', 'pull_request'],
            'jobs': {
                'build': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'uses': 'actions/checkout@v2'},
                        {
                            'uses': 'actions/steup-python@v2',
                            'with': {'python-version': '3.9'}
                        },
                        {'run': 'pip install -r requirements.txt'},
                        {'run': 'python -m unittest -vb test.py'}
                    ]
                }
            }
        }

        self.assertDictEqual(data, expected)
