#!/bin/sh

set -e

jupyter nbconvert --to notebook --execute tests-as-linear.ipynb
diff tests-as-linear.ipynb tests-as-linear.nbconvert.ipynb
DIFFEXIT=$?
rm -rf tests-as-linear.nbconvert.ipynb  # Clean up

if [ $DIFFEXIT -eq 0 ]
then
   echo "Tests passed!"
   exit 0
else
   echo "Notebook not executed in order. Rerun \`tests-as-linear.ipynb\`."
   exit 1
fi
