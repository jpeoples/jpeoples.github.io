find build/ -type f -name "*.html" | grep -v build/.git | sed -e "s/build/https:\/\/jpeoples.github.io/g" -e "s/index.html//g"
