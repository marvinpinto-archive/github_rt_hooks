#!/bin/bash
CURRDIR=$1
OUTFILE=$2
ldd $(find ${CURRDIR} -name '*.so') | grep -v ':$' | cut -d'(' -f1  | \
  sed -e 's@=>@\n@g'| \
  awk '{print $1}'| \
  sort | \
  uniq | \
  grep '^/'| \
  xargs yum provides > ${OUTFILE} 2>&1
