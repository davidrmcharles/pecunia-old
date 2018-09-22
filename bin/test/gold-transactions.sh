#!/bin/sh
#
# Replace the 'golden' shot of transactions.json with the current
# version.

thisdir="$( cd "$( dirname "$0" )" && pwd )"
basedir=$thisdir/../..
cp $basedir/private/transactions.json $basedir/private/gold/transactions.json
