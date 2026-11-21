import pandas as pd
from sqlalchemy import create_engine

# 数据库连接
engine = create_engine("mysql+pymysql://root:@127.0.0.1:3306/job_analysis?charset=utf8mb4")

# 读取爬虫生成的csv文件
df = pd.read_csv("data.csv", encoding="utf-8")

# 写入mysql job_info表
# if_exists="append" 追加；如果想要每次覆盖改成 replace
df.to_sql(
    name="job_info",
    con=engine,
    if_exists="append",
    index=False
)

print(f"成功导入 {len(df)} 条数据到 job_analysis.job_info")
