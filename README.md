# generative-ai-contest
### プロダクションションサーバーとパソコンを繋げる
#### 流れ
- hoge
```bash(on local)
# sshキーの作成
ssh-keygen -t ed25519 -C "your_email@example.com"
# パブリックキーの確認
cat ~/.ssh/id_ed25519.pub
```
```bash(on server)
# パブリックキーをサーバーに登録（管理者側の操作）
cd ~/.ssh/
echo "your_public_key" >> authorized_keys
```
```bash(on local)
# 接続の確認
ssh -i ~/.ssh/id_ed25519 ec2-user@server_ip_address
```
### プロダクションサーバーとgitを繋げる
#### 流れ
- hoge
```bash(on server)
# sshキーの作成
ssh-keygen -t ed25519 -C "your_email@example.com"
# パブリックキーの確認
cat ~/.ssh/id_ed25519.pub
```
githubの「アカウント」->「settings」->「SSH and GPG keys」->「New SSH key」からパブリックキーを登録

### プロダクションサーバー上でのリポジトリクローンの仕方
#### 流れ
- gitのインストール
- (プロダクションサーバーとgitが繋がっているか確認)
- リポジトリのクローン
```bash(on server)
# 
```
### Dockerの立ち上げ方
#### Dockerのインストール方法
```bash
sudo dnf install docker
sudo systemctl start docker
sudo systemctl enable docker
sudo docker run hello-world
sudo usermod -aG docker $USER
newgrp docker
```
#### DockerfileからDockerイメージを作成
```bash
# dockerファイルのあるディレクトリで
docker build -t gen-ai-contest-image:1.0 .
```
#### Dockerイメージからコンテナの作成
```bash
docker run -v .:/app -it gen-ai-contest-image:1.0 /bin/bash
```
#### コンテナの削除
```bash
# コンテナIDの確認
docker ps -a
# コンテナが停止していない場合
docker stop container_ID
# コンテナの削除
docker rm container_ID
```

### dockerコンテナにmysqlをインストールする方法
#### 流れ
1. インストールできるように諸々の設定を行う
1. apt updateで諸々の設定を反映させる
1. apt install mysql-serverで入れる

#### 前提条件
- dockerコンテナのOSはdebain系Linux
#### インストールのための設定
```bash
# MySQLのAPTリポジトリのダウンロード
wget https://dev.mysql.com/get/mysql-apt-config_0.8.32-1_all.deb
# パッケージのダウンロードに必要な依存パッケージ"lsb-release"のインストール
apt-get update
apt-get install -y lsb-release
# ダウンロードしたAPTリポジトリからパッケージをダウンロード
dpkg -i mysql-apt-config_0.8.32-1_all.deb
## 1. MySQL Server & Cluster (Currently selected: mysql-8.4-lts)
## 6. mysql-cluster-8.4-lts
## 3. OK
# MySQLサーバーとクライアントのインストール
apt-get update
apt-get install -y mysql-server mysql-client
## Enter root password: {hoge}
# MySQLのインストールが完了したか確認
mysql -V
## mysql  Ver 8.4.2-cluster for Linux on x86_64 (MySQL Cluster Community Server - GPL)
```
