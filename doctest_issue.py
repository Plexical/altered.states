def demo_doctest_issue():
    """
    >>> import sys
    >>> from altered import state, forget
    >>> with state(sys.modules, shutil=forget):
    ...     import shutil
    Traceback (most recent call last):
        ...
    KeyError: 'shutil'
    """
    import sys
    from altered import state, forget
    with state(sys.modules, shutil=forget):
        import shutil

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
