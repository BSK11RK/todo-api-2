# User登録
def test_register_user(client):
    res = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert res.status_code == 201
    
    data = res.json()
    
    assert data["email"] == "test@example.com"
    assert "id" in data
    
    # パスワードをレスポンスに返していないことを確認
    assert "password" not in data
    assert "hashed_password" not in data
    
    
# 重複登録
def test_register_duplicate_email(client):
    first_res = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )
    
    assert first_res.status_code == 201
    
    second_res = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )
    
    assert second_res.status_code == 400
    
    assert second_res.json() == {"detail": "Email already registered"}
    
    
# ログイン
def test_login(client):
    # ユーザー作成
    register_res = client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )
    
    assert register_res.status_code == 201
    
    res = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "password123"
        }
    )
    
    assert res.status_code == 200
    
    data = res.json()
    
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    
# 間違ったパスワード
def test_login_wrong_password(client):
    # ユーザーを作成
    register_res = client.post(
        "/auth/register",
        json={
            "email": "wrong-password@example.com",
            "password": "password123"
        }
    )
    
    assert register_res.status_code == 201
    
    # 間違ったパスワードでログイン
    res = client.post(
        "/auth/login",
        data={
            "username": "wrong-password@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert res.status_code == 401
    
    assert res.json() == {"detail": "Invalid email or password"}