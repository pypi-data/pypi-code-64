from sklearn.base import TransformerMixin
from sklearn.pipeline import _name_estimators
from collections import OrderedDict

all = [
    'Pipeline',
    'make_pipeline',
]

class Pipeline(TransformerMixin):
    def __init__(self, steps):
        self.steps = OrderedDict(steps)

    def fit(self, X):
        for i,step in enumerate(self.steps.values()):
            step.fit(X)
            if i < len(self.steps) - 1:
                X = step.transform(X)

    def fit_partial(self, X):
        for i,step in enumerate(self.steps.values()):
            step.fit_partial(X)
            if i < len(self.steps) - 1:
                X = step.transform(X)

    def transform(self, X):
        for step in self.steps.values():
            X = step.transform(X)
        return X


def make_pipeline(*steps):
    return Pipeline(_name_estimators(steps))