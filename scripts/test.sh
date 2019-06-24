#!/bin/sh

set -e

jupyter nbconvert --to notebook --execute tests-as-linear.ipynb
nbdiff --ignore-output tests-as-linear.ipynb tests-as-linear.nbconvert.ipynb > diff.txt

if [ -s diff.txt ]
then
   echo "Notebook not executed in order. Rerun \`tests-as-linear.ipynb\`."
   cat diff.txt
   rm -rf diff.txt tests-as-linear.nbconvert.ipynb  # Clean up
   exit 1
else
   echo "Tests passed!"
   rm -rf diff.txt tests-as-linear.nbconvert.ipynb  # Clean up
   exit 0
fi
