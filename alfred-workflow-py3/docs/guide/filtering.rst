
.. _filtering:

========================
Searching/filtering data
========================

.. currentmodule:: workflow

.. contents::
   :local:

Alfred gives you the option of letting it filter your results against the
user's query. Alfred uses "word starts with" matching, and can handle many
tens of thousands of results.

:meth:`Workflow.filter` provides a more sophisticated algorithm, similar to the
way Alfred matches applications with its default search (e.g. ``of`` will match
``OmniFocus``, which doesn't work with "Alfred filters results"). However, due
to being written in Python (a much slower language than Objective-C) and the
more complex algorithm, :meth:`Workflow.filter` becomes noticeably sluggish
with 1500–2500 items, depending on which options you've specified and the
speed of the Mac running the worklow.

If you have a very large dataset (20,000+ items) and/or need more sophisticated
matching than Alfred offers, I *strongly* recommend using
`sqlite and its fulltext search capability`_ to store and search your data.
It is smarter than :meth:`Workflow.filter` and *much* faster than "Alfred
filters results", handling hundreds of thousands of items with ease.


.. _alfred-filters-results:

Using "Alfred filters results"
==============================

"Alfred filters results" filters items based on their ``title`` field.
Alfred 3.5 introduced the ``match`` field, which if present, will be used
for filtering instead of ``title``.

You can set this field via the ``match`` parameter of the
:meth:`Workflow3.add_item()` method.


.. _fuzzy-filtering:

Fuzzy filtering with Alfred-Workflow
====================================

:meth:`Workflow.filter` provides a "fuzzy" search algorithm for filtering
your workflow's data. By default, :meth:`Workflow.filter` will try to match
your search query via CamelCase, substring, initials and all characters,
applying different weightings to the various kind of matches (see
:meth:`Workflow.filter` for a detailed description of the algorithm and match
flags).

Best practice is to do the following:

.. code-block:: python
    :linenos:

    def main(wf):

        query = None  # Ensure `query` is initialised

        # Set `query` if a value was passed (it may be an empty string)
        if len(wf.args):
            query = wf.args[0]

        items = load_my_items_from_somewhere()  # Load data from blah

        # If `query` is `None` or an empty string, all items are returned
        items = wf.filter(query, items)

        # Show error if there are no results. Otherwise, Alfred will show
        # its fallback searches (i.e. "Search Google for 'XYZ'")
        if not items:
            wf.add_item('No matches', icon=ICON_WARNING)

        # Generate list of results. If `items` is an empty list nothing happens
        for item in items:
            wf.add_item(item['title'], ...)

        wf.send_feedback()  # Send results to Alfred via STDOUT

This is by no means essential (``wf.args[0]`` will always be set if the script
is called from Alfred via ``python thescript.py "$1"``), but it *won't*
work from the command line unless called with an empty string
(``python thescript.py ""``), and it's good to be aware of when you're
dealing with unset/empty variables.


.. note::

    By default, :meth:`Workflow.filter`
    will match and return anything that contains all the characters in
    ``query`` in the same order, regardless of case. Not only can this lead to
    unacceptable performance when working with thousands of items, but it's
    also very likely that you'll want to set the standard a little higher.

    See :ref:`restricting-results` for info on how to do that.

To use :meth:`Workflow.filter`, pass it a query, a list of items to filter and
sort, and if your list contains items other than strings, a ``key`` function
that generates a string search key for each item:

.. code-block:: python
    :linenos:

    from workflow import Workflow

    names = ['Bob Smith', 'Carrie Jones', 'Harry Johnson', 'Sam Butterkeks']

    wf = Workflow()

    hits = wf.filter('bs', names)

Which returns::

    ['Bob Smith', 'Sam Butterkeks']

(``bs`` are Bob Smith's initials and ``Butterkeks`` contains both letters in that order.)


If your data are not strings:

.. code-block:: python
    :emphasize-lines: 11-12,16
    :linenos:

    from workflow import Workflow

    books = [
        {'title': 'A damn fine afternoon', 'author': 'Bob Smith'},
        {'title': 'My splendid adventure', 'author': 'Carrie Jones'},
        {'title': 'Bollards and other street treasures', 'author': 'Harry Johnson'},
        {'title': 'The horrors of Tuesdays', 'author': 'Sam Butterkeks'}
    ]


    def key_for_book(book):
        return '{} {}'.format(book['title'], book['author'])

    wf = Workflow()

    hits = wf.filter('bot', books, key_for_book)

Which returns::

    [{'author': 'Harry Johnson', 'title': 'Bollards and other street treasures'},
     {'author': 'Bob Smith', 'title': 'A damn fine afternoon'}]


.. _restricting-results:

Restricting results
-------------------

Chances are, you would not want ``bot`` to match ``Bob Smith A damn fine afternoon``
at all, or indeed any of the other books. Indeed, they have very low scores:

.. code-block:: python

    hits = wf.filter('bot', books, key_for_book, include_score=True)

produces::

    [({'author': 'Bob Smith', 'title': 'A damn fine afternoon'},
      11.11111111111111,
      64),
     ({'author': 'Harry Johnson', 'title': 'Bollards and other street treasures'},
      3.3333333333333335,
      64),
     ({'author': 'Sam Butterkeks', 'title': 'The horrors of Tuesdays'}, 3.125, 64)]

(``64`` is the rule that matched, :const:`~workflow.MATCH_ALLCHARS`,
which matches if all the characters in ``query`` appear in order in the search
key, regardless of case).

.. tip::

    ``rules`` in :meth:`~Workflow.filter` results are
    returned as integers. To see the name of the corresponding rule, see
    :ref:`matching-rules`.

If we filter ``{'author': 'Brienne of Tarth', 'title': 'How to beat up men'}`` and
``{'author': 'Zoltar', 'title': 'Battle of the Planets'}``, which we probably
would want to match ``bot``, we get::

    [({'author': 'Zoltar', 'title': 'Battle of the Planets'}, 98.0, 8),
     ({'author': 'Brienne of Tarth', 'title': 'How to beat up men'}, 90.0, 16)]

(The ranking would be reversed if ``key_for_book()`` returned ``author title``
instead of ``title author``.)

So in all likelihood, you'll want to pass a ``min_score`` argument to
:meth:`Workflow.filter`:

.. code-block:: python

    hits = wf.filter('bot', books, key_for_book, min_score=20)

and/or exclude some of the matching rules:

.. code-block:: python
    :linenos:

    from workflow import Workflow, MATCH_ALL, MATCH_ALLCHARS

    # [...]

    hits = wf.filter('bot', books, key_for_book, match_on=MATCH_ALL ^ MATCH_ALLCHARS)

You can set match rules using bitwise operators, so ``|`` to combine them or
``^`` to remove them from ``MATCH_ALL``:

.. code-block:: python
    :linenos:

    # match only CamelCase and initials
    match_on=MATCH_CAPITALS | MATCH_INITIALS

    # match everything but all-characters-in-item and substring
    match_on=MATCH_ALL ^ MATCH_ALLCHARS ^ MATCH_SUBSTRING

.. warning::

    ``MATCH_ALLCHARS`` is particularly slow and provides the
    worst matches. You should consider excluding it, especially if you're calling
    :meth:`Workflow.filter` with more than a
    few hundred items or expect multi-word queries.


.. _folding:

Diacritic folding
-----------------

By default, :meth:`Workflow.filter`
will fold non-ASCII characters to approximate ASCII equivalents (e.g. *é* >
*e*, *ü* > *u*) if ``query`` contains only ASCII characters. This behaviour
can be turned off by passing ``fold_diacritics=False`` to
:meth:`Workflow.filter`.

.. note::

    To keep the library small, only a subset of European languages are
    supported. The `Unidecode <https://pypi.python.org/pypi/Unidecode>`_ library
    should be used for comprehensive support of non-European alphabets.

Users may override a Workflow's default settings via ``workflow:folding…``
:ref:`magic arguments <magic-arguments>`.


.. _smart-punctuation:

"Smart" punctuation
^^^^^^^^^^^^^^^^^^^

The default diacritic folding only alters letters, not punctuation. If your
workflow also works with text that contains so-called "smart" (i.e. curly)
quotes or n- and m-dashes, you can use the :meth:`Workflow.dumbify_punctuation`
method to replace smart quotes and dashes with normal quotes and hyphens
respectively.


.. _matching-rules:

Matching rules
--------------

Here are the ``MATCH_*`` constants from :mod:`workflow` and their numeric values.

For a detailed description of the rules see :meth:`Workflow.filter`.


============================= =============================
Name                          Value
============================= =============================
``MATCH_STARTSWITH``          1
``MATCH_CAPITALS``            2
``MATCH_ATOM``                4
``MATCH_INITIALS_STARTSWITH`` 8
``MATCH_INITIALS_CONTAIN``    16
``MATCH_INITIALS``            24
``MATCH_SUBSTRING``           32
``MATCH_ALLCHARS``            64
``MATCH_ALL``                 127
============================= =============================


.. _sqlite and its fulltext search capability: https://github.com/deanishe/alfred-index-demo
