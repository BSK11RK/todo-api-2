import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


# テスト専用のSQLite DB
# メモリ上に作成するので、テスト終了後に消える
TEST_DATABASE_URL = "sqlite://"


test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False
)


@pytest.fixture
def db_session():
    # テスト1回ごとにDBを作成して、テスト終了後に削除する
    
    Base.metadata.create_all(bind=test_engine)
    
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)
        
        
@pytest.fixture
def client(db_session):
    # テスト用DBを使うTestClientを作成する
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
        
    
    # 本番用のget_dbをテスト用get_dbに置き換える
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
        
        # テスト終了後に元へ戻す
        app.dependency_overrides.clear()