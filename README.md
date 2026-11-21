# boss-zhipin-spider
BOSS直聘岗位数据采集可视化与AI岗位检索系统

## 项目介绍
本项目围绕招聘岗位真实数据展开，形成完整的数据链路闭环，分为五大模块：
1. 数据爬取：Reqable抓包定位接口，DrissionPage采集岗位数据，输出CSV原始数据
2. 数据预处理：空值过滤、薪资正则解析、技能文本清洗、分组统计
3. 数据库存储：db.py管理数据库连接，csv_to_mysql.py批量导入MySQL持久化存储
4. 数据可视化：Pyecharts绘制多类统计图表，Flask Web在线展示岗位分布、薪资情况
5. AI岗位检索：支持技能关键词模糊匹配，可筛选学历、薪资，返回匹配岗位列表

## 文件说明
- Boss.py：爬虫采集主程序
- csv_to_mysql.py：CSV数据入库脚本
- db.py：MySQL数据库连接配置
- load_data.py：数据读取与预处理
- visual.py：可视化绘图，生成job_visual.html
- ai_predict.py：AI岗位检索匹配逻辑
- app.py：Flask Web后端服务
- data.csv：采集得到的岗位样本数据
- job_visual.html：可视化图表页面
- requirements.txt：项目依赖包清单

## 运行步骤
1. 安装依赖：`pip install -r requirements.txt`
2. 修改 db.py 中的MySQL账号密码
3. 运行 Boss.py 采集岗位数据
4. 运行 csv_to_mysql.py 将数据导入数据库
5. 运行 visual.py 生成可视化图表
6. 运行 app.py，访问 http://127.0.0.1:5000 进入Web系统
