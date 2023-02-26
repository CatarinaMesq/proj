import pytest
from functions import *

@pytest.fixture
def app():
    """Instance of Main flask app"""
    return app()