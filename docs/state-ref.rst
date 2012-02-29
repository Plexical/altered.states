====================
 The state function
====================

.. py:function:: state(original[, change1=change1, changeN=changeN])

    A `ContextDecorator` that takes `original` and applies the changes
    sent as parameters and modifies `original` with these
    parameters. Upon completion it will restore `original` to the
    state it was before being called. Parameters can also have the
    marker value of :py:class:`forget` to temporary remove this name
    when :py:func:`state` is in effect.
