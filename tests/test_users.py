# JWTなしのテスト
def test_get_me_without_token(client):
    res = client.get("/users/me")
    
    assert res.status_code == 401
    
    
# JWTありのテスト
def test_get_me_with_token(client):
    # ユーザーを作成
    register_res = client.post(
        "/auth/register",
        json={
            "email": "me@example.com",
            "password": "password123"
        }
    )
    
    assert register_res.status_code == 201
    
    # ログイン
    login_res = client.post(
        "/auth/login",
        data={
            "username": "me@example.com",
            "password": "password123"
        }
    )
    
    assert login_res.status_code == 200
    
    token = login_res.json()["access_token"]
    
    # JWTをAuthorizationヘッダーに設定
    headers = {"Authorization": f"Bearer {token}"}
    
    # 現在のユーザーを取得
    res =client.get(
        "/users/me",
        headers=headers
    )
    
    assert res.status_code == 200
    
    data = res.json()
    
    assert data["email"] == "me@example.com"