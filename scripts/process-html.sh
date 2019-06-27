#!/bin/bash

# Embed Clicky web analytics.
LINE=9
head -n $LINE tests-as-linear.html > index.html
echo '<script>var clicky_site_ids = clicky_site_ids || []; clicky_site_ids.push(101159456);</script>' >> index.html
echo '<script async src="//static.getclicky.com/js"></script>' >> index.html
tail -n +$LINE tests-as-linear.html >> index.html

# Change title.
sed -i "s/<title>tests-as-linear<\/title>/<title>Common statistical tests are linear models (or: how to teach stats) | Eigenfoo<\/title>/" "index.html"
