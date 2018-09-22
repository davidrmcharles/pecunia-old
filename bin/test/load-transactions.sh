#!/bin/sh
#
# Replace the 'golden' shot of transactions.json with the current
# version.

thisdir="$( cd "$( dirname "$0" )" && pwd )"
basedir=$thisdir/../..
cp $basedir/private/gold/transactions.json $basedir/private/transactions.json
