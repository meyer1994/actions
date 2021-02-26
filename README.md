# pyactions

[![build](https://github.com/meyer1994/pyactions/actions/workflows/build.yml/badge.svg)](https://github.com/meyer1994/pyactions/actions/workflows/build.yml)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

A very silly proof of concept

## Table of Contents

- [About](#about)
- [Install](#install)
- [Usage](#usage)

## About

I've read [this][1] blog post on Reddit and tried to implement something that
could work as a configuration but has all the goods of a programming language.
I've used python because I am most proficient in it, but this could be created
in any language <sup>(maybe not intercal)</sup>.

This works by simply using python to generate a valid GitHub actions YAML file.
¯\\_(ツ)_/¯

## Install

```
pip install -r requirements.txt
```

## Usage

See this example. It generates an equivalent YAML to the one being used in this
repository right now.

```py
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
```

[1]: https://blog.earthly.dev/intercal-yaml-and-other-horrible-programming-languages/
