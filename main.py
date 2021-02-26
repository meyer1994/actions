from action import Action


class GitHubAction(Action):
    def configure(self):
        self.name = 'build'

        self.on = ['push', 'pull_request']

        with self.job('build') as j:
            j.runs_on = 'ubuntu-latest'

            j.uses('actions/checkout@v2')

            with j.uses('actions/steup-python@v2') as setup:
                setup['python-version'] = '3.9'

            j.run('pip install -r requirements.txt')
            j.run('python -m unittest -vb test.py')


action = GitHubAction()

yaml = action.yaml()
json = action.dict()
