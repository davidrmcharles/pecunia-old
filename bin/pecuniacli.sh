#!/bin/sh
#
# Invoke pecuniacli on (C) Python with an appropriately configured
# PYTHONPATH.

thisdir="$( cd "$( dirname "$0" )" && pwd )"
. $thisdir/../environment.sh
python/pecuniacli.py $@
