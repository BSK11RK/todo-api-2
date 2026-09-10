# Todo API

FastAPI、PostgreSQL、SQLAlchemy、JWT認証、Alembic、pytest、Docker Composeを使用して構築したTodo APIです。

バックエンド開発の学習を目的として、認証・認可、データベース設計、テスト、マイグレーション、コンテナ化まで一通り実装しています。

## 概要

ユーザー登録・ログイン機能を備えたTodo管理APIです。

JWTによる認証を行い、ログイン中のユーザー自身のTodoだけを取得・作成・更新・削除できるようにしています。

Todo一覧では、検索、完了状態によるフィルタリング、並び替え、ページネーションにも対応しています。

## 使用技術

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL
* psycopg
* pwdlib
* Argon2
* JWT
* PyJWT
* Alembic
* pytest
* Docker
* Docker Compose
* Git / GitHub

## 主な機能

### 認証

* ユーザー登録
* パスワードのハッシュ化
* ログイン
* JWTアクセストークン発行
* JWTによる認証
* 現在のユーザー情報取得

### ユーザー管理

* 自分のプロフィール取得
* メールアドレス変更
* パスワード変更
* アカウント削除

### Todo管理

* Todo作成
* Todo取得
* Todo更新
* Todo部分更新
* Todo削除
* ユーザーごとのTodo分離

### Todo一覧

* キーワード検索
* 完了状態によるフィルタリング
* 作成日時・更新日時による並び替え
* 昇順・降順
* ページネーション
* 総件数・総ページ数の取得

## API一覧

### Authentication

| Method | Endpoint         | Description |
| ------ | ---------------- | ----------- |
| POST   | `/auth/register` | ユーザー登録      |
| POST   | `/auth/login`    | ログイン・JWT発行  |

### Users

| Method | Endpoint    | Description |
| ------ | ----------- | ----------- |
| GET    | `/users/me` | 現在のユーザー取得   |
| PATCH  | `/users/me` | ユーザー情報更新    |
| DELETE | `/users/me` | アカウント削除     |

### Todos

| Method | Endpoint           | Description |
| ------ | ------------------ | ----------- |
| GET    | `/todos`           | Todo一覧取得    |
| GET    | `/todos/{todo_id}` | Todo取得      |
| POST   | `/todos`           | Todo作成      |
| PUT    | `/todos/{todo_id}` | Todo全体更新    |
| PATCH  | `/todos/{todo_id}` | Todo部分更新    |
| DELETE | `/todos/{todo_id}` | Todo削除      |

## Todo一覧API

`GET /todos` ではQuery Parameterを利用できます。

### 完了状態で絞り込み

```text
GET /todos?completed=false
```

### 検索

```text
GET /todos?search=FastAPI
```

タイトルと説明文を検索します。

### 並び替え

```text
GET /todos?sort=created_at&order=desc
```

使用できる `sort` は以下です。

* `created_at`
* `updated_at`

使用できる `order` は以下です。

* `asc`
* `desc`

### ページネーション

```text
GET /todos?page=1&limit=10
```

### 複数条件の組み合わせ

```text
GET /todos?search=FastAPI&completed=false&sort=updated_at&order=desc&page=1&limit=10
```

## Todo一覧レスポンス

```json
{
  "items": [
    {
      "id": 1,
      "title": "FastAPIを勉強する",
      "description": "JWTを理解する",
      "completed": false,
      "created_at": "2026-09-10T10:00:00+00:00",
      "updated_at": "2026-09-10T10:00:00+00:00"
    }
  ],
  "page": 1,
  "limit": 10,
  "total": 25,
  "total_pages": 3
}
```

## 認証

本APIではJWTによるBearer認証を使用しています。

### 1. ユーザー登録

```http
POST /auth/register
```

```json
{
  "email": "taro@example.com",
  "password": "password123"
}
```

### 2. ログイン

```http
POST /auth/login
```

ログイン成功後、アクセストークンが返されます。

```json
{
  "access_token": "xxxxx",
  "token_type": "bearer"
}
```

### 3. Authorization Header

認証が必要なAPIでは、以下のようにJWTを送信します。

```http
Authorization: Bearer <access_token>
```

## セキュリティ

パスワードは平文では保存せず、パスワードハッシュとしてDBへ保存しています。

ログイン時には入力されたパスワードを保存済みハッシュと検証し、認証成功後にJWTを発行します。

また、Todoには `user_id` を持たせ、ログイン中のユーザー自身のTodoのみ操作できるようにしています。

## データベース

PostgreSQLを使用しています。

UserとTodoは以下の関係です。

```text
User
  |
  | 1
  |
  | *
  v
Todo
```

Todoには `user_id` を持たせています。

主なTodoカラム：

```text
id
title
description
completed
user_id
created_at
updated_at
```

## プロジェクト構成

```text
todo-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   ├── dependencies.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── token.py
│   │   └── todo.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── root.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── todos.py
│   │
│   └── services/
│       ├── __init__.py
│       └── todo_service.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── conftest.py
│   ├── test_root.py
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_todos.py
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

## 環境変数

`.env` を作成し、以下の設定を行います。

```env
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql+psycopg://todo_user:todo_password@db:5432/todo_db
```

`.env` はGitHubへ公開しないように `.gitignore` へ追加しています。

## ローカル環境で起動

### Python環境で起動

依存関係をインストールします。

```bash
pip install -r requirements.txt
```

Alembicを実行します。

```bash
alembic upgrade head
```

FastAPIを起動します。

```bash
python -m uvicorn app.main:app --reload
```

Swagger UI：

```text
http://127.0.0.1:8000/docs
```

## Dockerで起動

Docker Composeを利用します。

```bash
docker compose build
```

```bash
docker compose up
```

バックグラウンドで起動する場合：

```bash
docker compose up -d
```

Swagger UI：

```text
http://127.0.0.1:8000/docs
```

## データベースマイグレーション

Alembicを使用してDBスキーマを管理しています。

### 最新のmigrationまで適用

```bash
alembic upgrade head
```

Docker環境では、

```bash
docker compose exec api alembic upgrade head
```

### migration作成

```bash
alembic revision --autogenerate -m "migration message"
```

自動生成されたmigrationは、内容を確認してから適用します。

## テスト

pytestを使用しています。

```bash
python -m pytest
```

Docker環境では、

```bash
docker compose exec api python -m pytest
```

テストでは、以下のようなケースを確認しています。

* ユーザー登録
* 重複メール登録
* ログイン
* 間違ったパスワード
* JWTなしでのアクセス
* 現在のユーザー取得
* Todo作成
* Todo一覧取得
* Todo検索
* フィルタリング
* 並び替え
* ページネーション
* 他ユーザーのTodoへのアクセス制御

## 開発で学んだこと

このプロジェクトでは、以下のバックエンド技術を実践しました。

* REST API設計
* FastAPI Router
* Pydanticによるバリデーション
* SQLAlchemyによるDB操作
* Foreign Key / Relationship
* パスワードハッシュ
* JWT認証
* Authentication / Authorization
* Dependency Injection
* Service層による責務分離
* pytestによるAPIテスト
* AlembicによるDBマイグレーション
* 環境変数による設定管理
* Docker / Docker Compose
* PostgreSQL

## 今後の改善候補

* CI/CDの導入
* エラーハンドリングの整理
* ロギング
* CORS設定
* Redisの導入
* 本番環境へのデプロイ
* PostgreSQLを利用した統合テスト
* APIドキュメントの改善
* パスワード変更APIの分離
* Refresh Tokenの導入

## About

このプロジェクトは、バックエンドエンジニアを目指すための学習・ポートフォリオとして作成したTodo APIです。

FastAPI、PostgreSQL、SQLAlchemy、JWT認証、pytest、Alembic、Docker Composeなどを使用し、バックエンド開発に必要な基本的な機能を実践的に実装しています。