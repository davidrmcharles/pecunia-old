#!/bin/sh
thisdir="$( cd "$( dirname "$0" )" && pwd )"
. $thisdir/../environment.sh
python/pecuniacli.py $@
