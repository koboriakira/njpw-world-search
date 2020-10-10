FROM python:3.8.6-slim

# 必要なパッケージをインストール
RUN apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y wget unzip curl gnupg
# 下の4つはGoogle ChromeDriverに必要なパッケージ
# libgconf-2-4 libnss3 libx11-6 libx11-xcb1

# Google Chrome ver86をインストール。Beta版にしか86がなかった
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  apt-get update && \
  apt-get install -y google-chrome-beta

WORKDIR /work

ADD Pipfile /work/Pipfile
ADD Pipfile.lock /work/Pipfile.lock
RUN pip install --upgrade pip && \
  pip install --no-cache-dir pipenv && \
  pipenv lock --dev -r > requirements.txt && \
  pip install --no-cache-dir -r requirements.txt


ADD njpw_world_search /work/njpw_world_search
ADD tests /work/tests

CMD ["uvicorn", "njpw_world_search.main:app", "--host", "0.0.0.0", "--port", "8080"]
