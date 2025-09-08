import pytest

@pytest.mark.dependency(depends=["test_a"])
def test_b():
    assert True
    
@pytest.mark.dependency()
def test_a():
    assert True