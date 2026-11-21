import re
from load_data import get_df
df = get_df()

def get_avg_salary(sal_text):
    nums = re.findall(r"\d+", str(sal_text))
    if len(nums) >= 2:
        return (int(nums[0]) + int(nums[1])) / 2
    return None

# 预处理薪资
df["薪资均值"] = df["薪资"].apply(get_avg_salary)
df_clean = df.dropna(subset=["薪资均值"])

def match_job(skill_keyword, edu_filter, exp_filter, sal_min, sal_max):
    tmp = df_clean.copy()

    # 学历筛选
    if edu_filter != "学历不限":
        tmp = tmp[tmp["学历"] == edu_filter]
    # 经验筛选（你的列名叫【经验】，不是工作经验！）
    if exp_filter != "经验不限":
        tmp = tmp[tmp["经验"] == exp_filter]
    # 薪资筛选
    tmp = tmp[(tmp["薪资均值"] >= sal_min) & (tmp["薪资均值"] <= sal_max)]

    # 技能关键词匹配，列名：所需技能
    skill_list = skill_keyword.strip().split()
    result = []
    for _, row in tmp.iterrows():
        skill_text = str(row["所需技能"]).lower()
        score = 0
        for sk in skill_list:
            if sk.lower() in skill_text:
                score += 1
        if skill_keyword.strip() == "" or score > 0:
            result.append({
                "岗位名称": row["职位"],
                "公司": row["公司"],
                "城市": row["城市"],
                "学历": row["学历"],
                "工作经验": row["经验"],
                "薪资": row["薪资"],
                "技能": row["所需技能"],
                "匹配分数": score
            })
    # 按匹配分降序
    result.sort(key=lambda x: x["匹配分数"], reverse=True)
    return result
