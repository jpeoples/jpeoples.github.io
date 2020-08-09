mkdir build
pushd build
git rm -rf .
git clean -fxd
git reset
popd
pipenv run python build.py
./generate_sitemap.sh > build/sitemap.txt
