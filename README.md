# 開発環境
## dokcer

- start docker app on local
- build
    ```
    cp .env{.sample,}
    docker-compose up -d --build --force-recreate
    '''
- check image name: `docker image ls`
- run in container: `docker run -p 5000:5000 -it anzan_batch python app.py`
- 適当なブラウザで `http://localhost:5000/`　にアクセスして確認

## local

- 実行: `python app.py`

# 本番環境
heroku

## トラブルシューティング
`heroku logs --app=anzan`
