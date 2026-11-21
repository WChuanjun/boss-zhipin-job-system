import pandas as pd
from sqlalchemy import create_engine

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "job_analysis",
    "charset": "utf8mb4"
}

def get_df():
    # 拼接sqlalchemy连接url
    url = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset=utf8mb4"
    engine = create_engine(url)
    df = pd.read_sql("SELECT * FROM job_info", engine)
    return df

# 使用示例：df = get_df()
