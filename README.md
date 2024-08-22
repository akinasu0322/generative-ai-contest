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
```bash(on server)
# sshキーの作成
ssh-keygen -t ed25519 -C "your_email@example.com"
# パブリックキーの確認
cat ~/.ssh/id_ed25519.pub
```
githubの「アカウント」->「settings」->「SSH and GPG keys」->「New SSH key」からパブリックキーを登録

### プロダクションサーバー上でのgitクローンの仕方
```bash(on server)
# 
```
### Dockerの立ち上げ方
#### DockerfileからDockerイメージを作成
```bash
# dockerファイルのあるディレクトリで
docker build -t gen-ai-contest-image:1.0 .
```
#### Dockerイメージからコンテナの作成
```bash
docker run -v .:/app -it gen-ai-contest-image:1.0 /bin/bash
```
