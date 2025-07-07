import os
import pytest

@pytest.fixture(autouse=True, scope='session')
def set_secret_key_env():
    os.environ['SECRET_KEY'] = 'test_secret_key' 