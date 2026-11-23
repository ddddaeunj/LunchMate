
import sqlite3
from pathlib import Path

# 데이터베이스 파일 경로
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "lunchmate.db"


# 데이터베이스 연결 함수
def get_connection():

    # data 폴더가 없으면 생성
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    # 외래 키 기능 활성화
    conn.execute("PRAGMA foreign_keys = ON")

    # 컬럼명을 이용한 데이터 접근 허용
    conn.row_factory = sqlite3.Row

    return conn


# 데이터베이스 테이블 생성 함수
def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # 그룹 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            invite_code TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 개인 사용자 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            budget INTEGER NOT NULL,
            allergies TEXT DEFAULT '[]',
            likes TEXT DEFAULT '[]',
            dislikes TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 구성원 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            budget INTEGER NOT NULL,
            allergies TEXT DEFAULT '[]',
            likes TEXT DEFAULT '[]',
            dislikes TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (group_id)
            REFERENCES groups(group_id)
            ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
