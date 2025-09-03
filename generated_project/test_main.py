import pytest
from main import hello_world  # Import the hello_world function

def test_hello_world():
    assert hello_world() == "Hello, World!"