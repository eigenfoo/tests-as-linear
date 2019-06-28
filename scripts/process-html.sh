#!/bin/bash

# Embed Clicky web analytics and Twitter card.
LINE=9
head -n $LINE tests-as-linear.html > index.html
echo '<script>var clicky_site_ids = clicky_site_ids || []; clicky_site_ids.push(101159456);</script>' >> index.html
echo '<script async src="//static.getclicky.com/js"></script>' >> index.html
echo '' >> index.html
echo '<meta name="twitter:card" content="summary_large_image">' >> index.html
echo '<meta name="twitter:site" content="@_eigenfoo">' >> index.html
echo '<meta name="twitter:creator" content="@_eigenfoo">' >> index.html
echo '<meta name="twitter:title" content="Common statistical tests are linear models: Python port">' >> index.html
echo '<meta name="twitter:image" content="https://eigenfoo.xyz/tests-as-linear/cheatsheets/linear_tests_cheat_sheet.png">' >> index.html
tail -n +$LINE tests-as-linear.html >> index.html

# Change title.
sed -i.bak "s/<title>tests-as-linear<\/title>/<title>Common statistical tests are linear models: Python port | Eigenfoo<\/title>/" "index.html"
rm index.html.bak
