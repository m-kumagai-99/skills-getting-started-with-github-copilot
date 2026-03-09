import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


_BASELINE_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_BASELINE_ACTIVITIES))
    yield


@pytest.fixture()
def client():
    with TestClient(app_module.app) as client:
        yield client
