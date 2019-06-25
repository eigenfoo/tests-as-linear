#!/bin/bash

LINE=9

head -n $LINE tests-as-linear.html > index.html
echo '<script>var clicky_site_ids = clicky_site_ids || []; clicky_site_ids.push(101159456);</script>' >> index.html
echo '<script async src="//static.getclicky.com/js"></script>' >> index.html
tail -n +$LINE tests-as-linear.html >> index.html

rm tests-as-linear.html
