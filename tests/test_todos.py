def test_create_todo(client):
    # ユーザーを作成
    register_res = client.post(
        "/auth/register",
        json={
            "email": "todo@example.com",
            "password": "password123"
        }
    )
    
    assert register_res.status_code == 201
    
    #  ログイン
    login_res = client.post(
        "/auth/login",
        data={
            "username": "todo@example.com",
            "password": "password123"
        }
    )
    
    assert login_res.status_code == 200
    
    token = login_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Todo作成
    res = client.post(
        "/todos",
        json={
            "title": "FastAPIを勉強する",
            "description": "pytestを勉強する",
            "completed": False
        },
        headers=headers
    )
    
    assert res.status_code == 201
    
    data = res.json()
    
    assert data["title"] == "FastAPIを勉強する"
    assert data["description"] == "pytestを勉強する"
    assert data["completed"] is False
    
    
# Todo一覧取得をテスト
def test_get_todos(client):
    # ユーザーを作成
    register_res = client.post(
        "/auth/register",
        json={
            "email": "list@example.com",
            "password": "password123"
        }
    )

    assert register_res.status_code == 201

    # ログイン
    login_res = client.post(
        "/auth/login",
        data={
            "username": "list@example.com",
            "password": "password123"
        }
    )

    assert login_res.status_code == 200

    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Todo作成
    client.post(
        "/todos",
        json={
            "title": "Todo 1",
            "description": "説明1",
            "completed": False
        },
        headers=headers
    )

    client.post(
        "/todos",
        json={
            "title": "Todo 2",
            "description": "説明2",
            "completed": True
        },
        headers=headers
    )

    # Todo取得
    res = client.get("/todos", headers=headers)

    assert res.status_code == 200

    data = res.json()

    assert len(data["items"]) == 2
    assert data["items"][0]["title"] == "Todo 2"
    assert data["items"][1]["title"] == "Todo 1"
    
    
# 他のユーザーのTodoを操作できないことをテスト
def test_user_cannot_access_other_users_todo(client):
    # User Aを作成
    client.post(
        "/auth/register",
        json={
            "email": "user-a@example.com",
            "password": "password123"
        }
    )

    login_a = client.post(
        "/auth/login",
        data={
            "username": "user-a@example.com",
            "password": "password123"
        }
    )

    assert login_a.status_code == 200

    token_a = login_a.json()["access_token"]

    headers_a = {"Authorization": f"Bearer {token_a}"}

    # User AのTodoを作成
    create_res = client.post(
        "/todos",
        json={
            "title": "User AのTodo",
            "description": "User Aだけが見られる",
            "completed": False
        },
        headers=headers_a
    )

    assert create_res.status_code == 201

    todo_id = create_res.json()["id"]

    # User Bを作成
    client.post(
        "/auth/register",
        json={
            "email": "user-b@example.com",
            "password": "password123"
        }
    )

    login_b = client.post(
        "/auth/login",
        data={
            "username": "user-b@example.com",
            "password": "password123"
        }
    )

    assert login_b.status_code == 200

    token_b = login_b.json()["access_token"]

    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User BがUser AのTodoを取得
    res = client.get(
        f"/todos/{todo_id}",
        headers=headers_b
    )

    assert res.status_code == 404
    
    
# Timestamp
def test_todo_has_timestamps(client):
    # ユーザー作成
    register_response = client.post(
        "/auth/register",
        json={
            "email": "timestamp@example.com",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    # ログイン
    login_response = client.post(
        "/auth/login",
        data={
            "username": "timestamp@example.com",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Todo作成
    response = client.post(
        "/todos",
        json={
            "title": "Timestamp Test",
            "description": "日時を確認する",
            "completed": False
        },
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert "created_at" in data
    assert "updated_at" in data
    assert data["created_at"] is not None
    assert data["updated_at"] is not None
    
    
# updated_atの更新
def test_todo_updated_at_changes(client):
    # ユーザー作成
    client.post(
        "/auth/register",
        json={
            "email": "updated@example.com",
            "password": "password123"
        }
    )

    # ログイン
    login_response = client.post(
        "/auth/login",
        data={
            "username": "updated@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Todo作成
    create_response = client.post(
        "/todos",
        json={
            "title": "Original",
            "description": "Original description",
            "completed": False
        },
        headers=headers,
    )

    todo = create_response.json()

    todo_id = todo["id"]
    created_at = todo["created_at"]
    updated_at = todo["updated_at"]

    # Todo更新
    update_response = client.patch(
        f"/todos/{todo_id}",
        json={
            "completed": True,
        },
        headers=headers
    )

    assert update_response.status_code == 200

    updated_todo = update_response.json()

    assert updated_todo["created_at"] == created_at
    assert updated_todo["updated_at"] >= updated_at
    
    
# 絞り込み（フィルタリング）
def test_get_todos_by_completed(client):
    # ユーザー作成
    client.post(
        "/auth/register",
        json={
            "email": "filter@example.com",
            "password": "password123"
        }
    )
    
    # ログイン
    login_res = client.post(
        "/auth/login",
        data={
            "username": "filter@example.com",
            "password": "password123"
        }
    )
    
    assert login_res.status_code == 200
    
    token = login_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 未完了Todo
    client.post(
        "/todos",
        json={
            "title": "未完了Todo",
            "description": "まだ終わっていない",
            "completed": False
        },
        headers=headers
    )
    
    # 完了Todo
    client.post(
        "/todos",
        json={
            "title": "完了Todo",
            "description": "終わった",
            "completed": True
        },
        headers=headers
    )
    
    # 未完了だけ取得
    res = client.get(
        "/todos?completed=false",
        headers=headers
    )
    
    assert res.status_code == 200
    
    data = res.json()
    
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "未完了Todo"
    assert data["items"][0]["completed"] is False
    
    
# 並び替え
def test_get_todos_sort_by_created_at(client):
    # ユーザー作成
    client.post(
        "/auth/register",
        json={
            "email": "sort@example.com",
            "password": "password123"
        }
    )

    # ログイン
    login_res = client.post(
        "/auth/login",
        data={
            "username": "sort@example.com",
            "password": "password123"
        }
    )

    assert login_res.status_code == 200

    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Todo 1
    res_1 = client.post(
        "/todos",
        json={
            "title": "Todo 1",
            "description": "最初に作成",
            "completed": False
        },
        headers=headers
    )

    assert res_1.status_code == 201

    # Todo 2
    res_2 = client.post(
        "/todos",
        json={
            "title": "Todo 2",
            "description": "後に作成",
            "completed": False
        },
        headers=headers
    )

    assert res_2.status_code == 201

    # 新しい順で取得
    res = client.get(
        "/todos?sort=created_at&order=desc",
        headers=headers
    )

    assert res.status_code == 200

    data = res.json()

    assert data["total"] == 2
    assert data["total_pages"] == 1
    assert len(data["items"]) == 2

    assert data["items"][0]["title"] == "Todo 2"
    assert data["items"][1]["title"] == "Todo 1"
    
    
# 古い順
def test_get_todos_sort_by_created_at_asc(client):
    client.post(
        "/auth/register",
        json={
            "email": "sort-asc@example.com",
            "password": "password123",
        },
    )

    login_res = client.post(
        "/auth/login",
        data={
            "username": "sort-asc@example.com",
            "password": "password123"
        }
    )

    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/todos",
        json={
            "title": "Todo 1",
            "description": "最初",
            "completed": False
        },
        headers=headers
    )

    client.post(
        "/todos",
        json={
            "title": "Todo 2",
            "description": "後",
            "completed": False
        },
        headers=headers
    )

    res = client.get(
        "/todos?sort=created_at&order=asc",
        headers=headers
    )

    assert res.status_code == 200

    data = res.json()

    assert data["total"] == 2
    assert data["total_pages"] == 1
    assert len(data["items"]) == 2

    assert data["items"][0]["title"] == "Todo 1"
    assert data["items"][1]["title"] == "Todo 2"
    
    
# ページネーション
def test_get_todos_pagination(client):
    # ユーザー作成
    client.post(
        "/auth/register",
        json={
            "email": "pagination@example.com",
            "password": "password123"
        }
    )
    
    # ログイン
    login_res = client.post(
        "/auth/login",
        data={
            "username": "pagination@example.com",
            "password": "password123"
        }
    )
    
    token = login_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Todoを5件作成
    for i in range(1, 6):
        res = client.post(
            "/todos",
            json={
                "title": f"Todo {i}",
                "description": f"Description {i}",
                "completed": False
            },
            headers=headers
        )
        
        assert res.status_code == 201
        
    # 1ページ2件
    res = client.get(
        "/todos?page=1&limit=2",
        headers=headers
    )

    assert res.status_code == 200

    data = res.json()

    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["total"] == 5
    assert data["total_pages"] == 3

    assert len(data["items"]) == 2
    assert data["items"][0]["title"] == "Todo 5"
    assert data["items"][1]["title"] == "Todo 4"

    # 2ページ目
    res = client.get(
        "/todos?page=2&limit=2",
        headers=headers
    )

    assert res.status_code == 200

    data = res.json()

    assert data["page"] == 2
    assert len(data["items"]) == 2
    assert data["items"][0]["title"] == "Todo 3"
    assert data["items"][1]["title"] == "Todo 2"

    # 3ページ目
    res = client.get(
        "/todos?page=3&limit=2",
        headers=headers
    )

    assert res.status_code == 200

    data = res.json()

    assert data["page"] == 3
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Todo 1"
    
    
# 検索
def test_search_todos(client):
    # ユーザー作成
    client.post(
        "/auth/register",
        json={
            "email": "search@example.com",
            "password": "password123"
        }
    )

    # ログイン
    login_res = client.post(
        "/auth/login",
        data={
            "username": "search@example.com",
            "password": "password123"
        }
    )

    assert login_res.status_code == 200

    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Todo 1
    client.post(
        "/todos",
        json={
            "title": "FastAPIを勉強する",
            "description": "JWTを勉強する",
            "completed": False
        },
        headers=headers
    )

    # Todo 2
    client.post(
        "/todos",
        json={
            "title": "Dockerを勉強する",
            "description": "FastAPIをコンテナ化する",
            "completed": False
        },
        headers=headers
    )

    # Todo 3
    client.post(
        "/todos",
        json={
            "title": "買い物をする",
            "description": "スーパーに行く",
            "completed": False
        },
        headers=headers
    )

    # FastAPIで検索
    res = client.get(
        "/todos?search=FastAPI",
        headers=headers
    )

    assert res.status_code == 200

    data = res.json()

    assert len(data["items"]) == 2

    titles = {
        todo["title"]
        for todo in data["items"]
    }

    assert "FastAPIを勉強する" in titles
    assert "Dockerを勉強する" in titles
    assert "買い物をする" not in titles