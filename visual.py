from load_data import get_df
import re
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Line, WordCloud, Page
from pyecharts.globals import ThemeType

df = get_df()

# 薪资清洗函数，提取薪资下限、上限，算均值
def get_avg_salary(sal_text):
    if not sal_text:
        return None
    nums = re.findall(r"\d+", sal_text)
    if len(nums) >= 2:
        return (int(nums[0]) + int(nums[1])) / 2
    return None

df["薪资均值"] = df["薪资"].apply(get_avg_salary)
df_clean = df.dropna(subset=["薪资均值"])

# 1.城市岗位柱状图
city_cnt = df["城市"].value_counts().reset_index()
bar_city = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(city_cnt["城市"].tolist())
    .add_yaxis("岗位数量", city_cnt["count"].tolist())
    .set_global_opts(title_opts=opts.TitleOpts(title="各城市岗位数量"))
)

#2.学历分布饼图
edu_cnt = df["学历"].value_counts().reset_index()
pie_edu = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add("", list(zip(edu_cnt["学历"], edu_cnt["count"])), radius=["30%", "75%"])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="学历要求分布")
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
)

# 3.学历-平均薪资柱状图
edu_order = ["学历不限", "中专/中技", "高中", "大专", "本科", "硕士", "博士"]
# 按指定顺序筛选、分组取均值
edu_sal_df = df_clean.groupby("学历")["薪资均值"].mean().reindex(edu_order).reset_index()
# 剔除NaN（如果某个学历没有数据）
edu_sal_df = edu_sal_df.dropna()

x_edu = edu_sal_df["学历"].tolist()
y_edu = edu_sal_df["薪资均值"].round(2).tolist()

bar_sal = (
    Bar()
    .add_xaxis(x_edu)
    .add_yaxis("平均薪资", y_edu)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="不同学历平均薪资"),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=-30)
        )
    )
)

# 4.工作经验折线图
x_exp = ["经验不限", "在校/应届", "1年以内", "1-3年", "3-5年", "5-10年"]
y_exp = [83, 29, 5, 114, 159, 52]
line_exp = (
    Line()
    .add_xaxis(["经验不限", "在校/应届", "1年以内", "1-3年", "3-5年", "5-10年"])
    .add_yaxis("岗位数", [83, 29, 5, 114, 159, 52])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="工作经验需求分布"),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(rotate=-30)
        )
    )
)

#5.企业规模环形饼图
scale_cnt = df["规模"].value_counts().reset_index()
pie_scale = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add("", list(zip(scale_cnt["规模"], scale_cnt["count"])), radius=["40%", "70%"])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="企业规模分布")
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
)

#6.技能词云
from collections import Counter

# 内置基础技术词典，用于切割粘连字符串（程序自动在这里匹配拆分）
tech_dict = {
    "Python", "Java", "C++", "C#", "QT", "MySQL", "Redis", "Oracle", "MongoDB",
    "PostgreSQL", "SpringCloud", "SpringBoot", "MyBatis", "Nginx", "Docker",
    "TensorFlow", "PyTorch", "JavaScript", "Vue", "React", "Angular", "Django",
    "Flask", "Spark", "Hadoop", "Hive", "Netty", "STL", "MFC", "Linux", "Windows",
    "机器学习", "深度学习", "数据标注", "自动化测试", "计算机视觉", "微服务", "分布式"
}
# 按字符串长度倒序，优先匹配长词，避免短词优先匹配
tech_list = sorted(tech_dict, key=lambda x: len(x), reverse=True)

def split_concat_text(s):
    """自动切割粘连的技术文本，返回拆分后的词列表"""
    res = []
    i = 0
    n = len(s)
    while i < n:
        matched = None
        for w in tech_list:
            if s.startswith(w, i):
                matched = w
                break
        if matched:
            res.append(matched)
            i += len(matched)
        else:
            i += 1
    return res

skill_list = df["所需技能"].dropna().astype(str).tolist()
skill_all = " ".join(skill_list)
# 先把所有内容按正则切成一块块候选串
pattern = re.compile(r"[\u4e00-\u9fa5]+|[A-Za-z0-9+\#\.]+")
raw_tokens = pattern.findall(skill_all)

all_words = []
for token in raw_tokens:
    sub_words = split_concat_text(token)
    all_words.extend(sub_words)

# 过滤停用词
stop = {"Windows", "Server", "API", "IT", "act", "adas", "3c", "SLG"}
valid = [w for w in all_words if len(w)>=2 and w not in stop]

counter = Counter(valid)
wc_data = counter.most_common(60)  # 取频次最高60个，不会太拥挤

wc = (
    WordCloud(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add("", wc_data, word_size_range=[10, 90])
    .set_global_opts(title_opts=opts.TitleOpts(title="岗位技能词云"))
)


# 布局
# 方案：每个图表单独渲染，再手写一个html，用flex实现一行2个
chart_map = {
    "city": bar_city,
    "edu_sal": bar_sal,
    "exp": line_exp,
    "edu_pie": pie_edu,
    "scale_pie": pie_scale,
    "wordcloud": wc
}


