#!/bin/sh

jupyter nbconvert --to notebook --execute tests-as-linear.ipynb
nbdiff --ignore-output tests-as-linear.ipynb tests-as-linear.nbconvert.ipynb > ipynb.diff
jupyter nbconvert --to html tests-as-linear.nbconvert.ipynb
diff index.html tests-as-linear.nbconvert.html > html.diff

if [ -s ipynb.diff ]
then
   echo "Notebook not executed in order. Rerun notebook."
   cat ipynb.diff
   exit 1
else
   rm -rf ipynb.diff tests-as-linear.nbconvert.ipynb
   echo "Notebook executed in order!"
fi

DIFFSIZE=$(cat html.diff | wc -l)
if [ $DIFFSIZE -gt 10 ]
then
   echo "HTML does not match notebook. Republish."
   cat html.diff
   exit 1
else
   rm -rf html.diff tests-as-linear.nbconvert.html
   echo "HTML matches notebook!"
fi

exit 0
