import pymysql
from sqlalchemy import create_engine
import pandas as pd

# 数据库配置
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "job_analysis",
    "charset": "utf8mb4"
}

# 引擎，用于pandas读写
engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset=utf8mb4"
)

# 创建数据表
def create_table():
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS job_info (
        id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
        职位 VARCHAR(255),
        学历 VARCHAR(50),
        经验 VARCHAR(50),
        薪资 VARCHAR(50),
        所需技能 TEXT,
        城市 VARCHAR(50),
        区域 VARCHAR(100),
        商业区 VARCHAR(100),
        经度 DOUBLE,
        纬度 DOUBLE,
        公司 VARCHAR(255),
        领域 VARCHAR(255),
        规模 VARCHAR(100),
        性质 VARCHAR(100),
        福利 TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

# 写入df到mysql（追加写入，不会重复）
def save_to_mysql(df):
    df.to_sql(name="job_info", con=engine, if_exists="append", index=False)

# 读取全部数据返回df
def read_from_mysql():
    df = pd.read_sql("select * from job_info", con=engine)
    return df

if __name__ == "__main__":
    create_table()
    print("数据表创建完成")
