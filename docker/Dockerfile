FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なファイルをコピー
COPY . /app

# 必要なシステムコマンドのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    wget \
    expect \
    && rm -rf /var/lib/apt/lists/*

# MySQLのインストール
RUN /app/docker/_install_mysql.sh


# 必要なPythonライブラリをインストール
COPY ./docker/requirements.txt /app/docker
RUN pip install --no-cache-dir -r /app/docker/requirements.txt

