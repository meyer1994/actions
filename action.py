from copy import deepcopy
from typing import List, Dict
from abc import ABC, abstractmethod
from contextlib import contextmanager, AbstractContextManager

import yaml


class Base(ABC):
    @abstractmethod
    def dict(self) -> dict:
        pass

    def yaml(self) -> str:
        data = self.dict()
        return yaml.dump(data)


class Step(Base, AbstractContextManager):
    def __init__(self):
        super(Step, self).__init__()
        self.run: str = None
        self.uses: str = None
        self.wth: Dict[str, str] = {}

    def dict(self) -> dict:
        if self.uses is None:
            return {'run': self.run}

        if self.wth == {}:
            return {'uses': self.uses}

        return {
            'uses': self.uses,
            'with': deepcopy(self.wth)
        }

    def __setitem__(self, name: str, val: str):
        self.wth[name] = val

    def __enter__(self):
        return self

    def __exit__(self, typ: type, val: object, exc: Exception):
        pass


class Job(Base):
    def __init__(self):
        super(Job, self).__init__()
        self.runs_on: str = None
        self.steps: List[Step] = []

    def dict(self) -> dict:
        return {
            'runs-on': self.runs_on,
            'steps': [s.dict() for s in self.steps]
        }

    def uses(self, action: str) -> Step:
        step = Step()
        step.uses = action
        self.steps.append(step)
        return step

    def run(self, cmd: str) -> Step:
        step = Step()
        step.run = cmd
        self.steps.append(step)


class Action(Base):
    def __init__(self):
        super(Action, self).__init__()
        self.name: str = None
        self.on: List[str] = []
        self.jobs: Dict[str, Job] = {}
        self.configure()

    def dict(self) -> dict:
        return {
            'name': self.name,
            'on': deepcopy(self.on),
            'jobs': {k: v.dict() for k, v in self.jobs.items()}
        }

    def configure(self):
        pass

    @contextmanager
    def job(self, name: str) -> Job:
        self.jobs[name] = Job()
        yield self.jobs[name]
