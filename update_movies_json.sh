cd ~/git/njpw-world-search && \
source .venv/bin/activate && \
python -m generate_json && \
git add movies.json && \
git cm "Auto update movies.json" && \
git push
# cp movies.json /Users/canary/git/njpw-world-search-front/src/json/movies.json && \
# cd ~/git/njpw-world-search-front && \
# git add src/json/movies.json && \
# git cm "Auto update movies.json" && \
# git push
