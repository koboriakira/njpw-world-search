cd ~/git/njpw-world-search && \
source .venv/bin/activate && \
python -m generate_json && \
git add movies.json && \
git cm "Auto update movies.json" && \
git push
