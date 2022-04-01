
.. _icons:

============
System icons
============

The :mod:`~workflow.workflow` module provides access to a number of default
macOS icons via ``ICON_*`` constants for use when generating Alfred feedback:

.. code-block:: python
    :linenos:

    from workflow import Workflow, ICON_INFO

    wf = Workflow()
    wf.add_item('For your information', icon=ICON_INFO)
    wf.send_feedback()


.. _icon-list:

List of icons
=============

These are all the icons accessible in :mod:`~workflow.workflow`. They (and
more) can be found in
``/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/``.

+-------------------+----------------------------------------+
| Name              | Preview                                |
+===================+========================================+
|``ICON_ACCOUNT``   |.. image:: ../_static/ICON_ACCOUNT.png  |
+-------------------+----------------------------------------+
|``ICON_BURN``      |.. image:: ../_static/ICON_BURN.png     |
+-------------------+----------------------------------------+
|``ICON_CLOCK``     |.. image:: ../_static/ICON_CLOCK.png    |
+-------------------+----------------------------------------+
|``ICON_COLOR``     |.. image:: ../_static/ICON_COLOR.png    |
+-------------------+----------------------------------------+
|``ICON_COLOUR``    |.. image:: ../_static/ICON_COLOUR.png   |
+-------------------+----------------------------------------+
|``ICON_EJECT``     |.. image:: ../_static/ICON_EJECT.png    |
+-------------------+----------------------------------------+
|``ICON_ERROR``     |.. image:: ../_static/ICON_ERROR.png    |
+-------------------+----------------------------------------+
|``ICON_FAVORITE``  |.. image:: ../_static/ICON_FAVORITE.png |
+-------------------+----------------------------------------+
|``ICON_FAVOURITE`` |.. image:: ../_static/ICON_FAVOURITE.png|
+-------------------+----------------------------------------+
|``ICON_GROUP``     |.. image:: ../_static/ICON_GROUP.png    |
+-------------------+----------------------------------------+
|``ICON_HELP``      |.. image:: ../_static/ICON_HELP.png     |
+-------------------+----------------------------------------+
|``ICON_HOME``      |.. image:: ../_static/ICON_HOME.png     |
+-------------------+----------------------------------------+
|``ICON_INFO``      |.. image:: ../_static/ICON_INFO.png     |
+-------------------+----------------------------------------+
|``ICON_NETWORK``   |.. image:: ../_static/ICON_NETWORK.png  |
+-------------------+----------------------------------------+
|``ICON_NOTE``      |.. image:: ../_static/ICON_NOTE.png     |
+-------------------+----------------------------------------+
|``ICON_SETTINGS``  |.. image:: ../_static/ICON_SETTINGS.png |
+-------------------+----------------------------------------+
|``ICON_SWIRL``     |.. image:: ../_static/ICON_SWIRL.png    |
+-------------------+----------------------------------------+
|``ICON_SWITCH``    |.. image:: ../_static/ICON_SWITCH.png   |
+-------------------+----------------------------------------+
|``ICON_SYNC``      |.. image:: ../_static/ICON_SYNC.png     |
+-------------------+----------------------------------------+
|``ICON_TRASH``     |.. image:: ../_static/ICON_TRASH.png    |
+-------------------+----------------------------------------+
|``ICON_USER``      |.. image:: ../_static/ICON_USER.png     |
+-------------------+----------------------------------------+
|``ICON_WARNING``   |.. image:: ../_static/ICON_WARNING.png  |
+-------------------+----------------------------------------+
|``ICON_WEB``       |.. image:: ../_static/ICON_WEB.png      |
+-------------------+----------------------------------------+

If you'd like other standard macOS icons to be added, please
`add an issue on GitHub`_.

.. _add an issue on GitHub: https://github.com/deanishe/alfred-workflow/issues
