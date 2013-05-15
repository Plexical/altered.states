====================
 The alter function
====================

.. py:function:: alter(original[, change1=change1, changeN=changeN])

    Modified `original` and applies the changes sent as
    parameters. Parameters can also have the marker value of
    :py:class:`forget` to temporary remove this name while the changes
    are in effect.

    Returns a new function that will reverse the effect of itself.
