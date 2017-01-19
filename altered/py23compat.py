def strio():
    """
    This was difficult to get right in doctests when porting to Python 3.
    """
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
    return StringIO()
