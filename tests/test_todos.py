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
        headers=headers,
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

    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"
    
    
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