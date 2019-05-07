======================================================================
``README`` for ``pecunia``
======================================================================

Import and analyze bank-account activity

* `Import transactions`_
* `List transactions`_

  * `By date`_
  * `By description`_

Import transactions
======================================================================

Before we can do anything else, we must import transactions into the
database.  Achieve this with the ``import`` subcommand of
``pecuniacli``::

    bin/pecuniacli.sh import FILE

List transactions
======================================================================

List imported transactions with the ``list`` subcommand of
``pecuniacli``::

    bin/pecuniacli.sh list

The ``list`` subcommand has several options to filter transactions by
various criteria such as date and description.

By date
----------------------------------------------------------------------

Filter the list of transactions by date with the ``--dates`` option.
Express dates in ``YYYY-MM-DD`` format.  Separate the first and last
dates of a range of dates with a two periods (``..``).  You may
express an 'open' date range by either leading or following a date
with two periods (``..``).

To see only transactions on a particular date::

    bin/pecuniacli.sh list --dates=2019-05-06

To see only transactions in a date range::

    bin/pecuniacli.sh list --dates=2019-05-06..2019-05-07

To see only transactions *on and following* a date::

    bin/pecuniacli.sh list --dates=2019-05-06..

To see only transactions *before and on* a date::

    bin/pecuniacli.sh list --dates=..2019-05-06

You may also chain together dates and date ranges with commas like
so::

    bin/pecuniacli.sh list --dates=2019-05-01,2019-05-03..2019-05-05

By description
----------------------------------------------------------------------

Filter the list of transactions by description with the ``--include``
and ``--exclude`` options.  Both options accept a regular expression
to match against the transaction descriptions.  You may provide both
options repeatedly to provide multiple regular expressions.  However,
``--include`` and ``--exclude`` are mutually exclusive of each other.

To see only transactions with a description matching a pattern::

    bin/pecuniacli.sh list --include=amazon

To see only transactions matching one of two patterns::

    bin/pecuniacli.sh list --include=foo --include=bar

To see only transactions not matching a pattern::

    bin/pecuniacli.sh list --exclude=zod
