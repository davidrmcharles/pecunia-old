#!/bin/sh
#
# Diff the 'golden' snapshot of transactions.json to the current
# version.

thisdir="$( cd "$( dirname "$0" )" && pwd )"
basedir=$thisdir/../..
diff $basedir/private/gold/transactions.json $basedir/private/transactions.json
