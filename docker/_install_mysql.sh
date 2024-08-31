#!/bin/bash

# 1. MySQLのAPTリポジトリのダウンロード
echo "Downloading MySQL APT repository package..."
wget https://dev.mysql.com/get/mysql-apt-config_0.8.32-1_all.deb

# 2. パッケージのダウンロードに必要な依存パッケージ"lsb-release"のインストール
echo "Updating package lists and installing lsb-release..."
apt-get update
apt-get install -y lsb-release

# 3. ダウンロードしたAPTリポジトリからパッケージをダウンロード
echo "Configuring MySQL APT repository..."
/app/docker/_download_mysql-apt-config.exp # dpkg -i mysql-apt-config_0.8.32-1_all.deb に相当
rm mysql-apt-config_0.8.32-1_all.deb

# 5. MySQLサーバーとクライアントのインストール
echo "Installing MySQL server and client..."
apt-get update
/app/docker/_install_mysql-server.exp # apt-get install mysql-server に相当
apt-get install -y mysql-client

# 6. MySQLのインストールが完了したか確認
echo "Verifying MySQL installation..."
mysql -V

echo "MySQL installation and configuration completed successfully!"
