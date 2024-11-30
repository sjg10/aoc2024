def pytest_collection_modifyitems(items):
    """Ensure the tests are all run in alphabetical order"""
    items.sort(key=lambda x: f"{x.module.__name__}.{x.name}")
