mkdir build_local
pushd build_local
rm -rf *
popd
pipenv run python build.py local
./generate_sitemap.sh > build_local/sitemap.txt
cd build_local
python -m http.server 8080
