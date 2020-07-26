pushd build
git rm -rf .
git clean -fxd
git reset
popd
pipenv run python build.py local
./generate_sitemap.sh > build/sitemap.txt
cd build
python -m http.server 8080
