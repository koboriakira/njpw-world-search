cd ~/git/njpw-world-search && \
python -m njpw_world_search.generate_json && \
cp movies.json /Users/canary/git/njpw-world-search-front/src/json/movies.json && \
cd ~/git/njpw-world-search-front && \
git add src/json/movies.json && \
git cm "Auto update movies.json" && \
git push
