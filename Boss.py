#导入自动化模块
import json
from DrissionPage import ChromiumPage
#导入格式化输出模块
from pprint import pprint
#导入csv模块
import csv

#创建文件
f = open('data.csv',mode = 'w',encoding = 'utf-8',newline='')
#字典写入方法
csv_writer = csv.DictWriter(f,fieldnames = [
        '职位',
        '学历',
        '经验',
        '薪资',
        '所需技能',
        '城市',
        '区域',
        '商业区',
        '经度',
        '纬度',
        '公司',
        '领域',
        '规模',
        '性质',
        '福利',
])
#写入表头
csv_writer.writeheader()

#打开浏览器
dp = ChromiumPage()
#监听数据
dp.listen.start('joblist')
#访问网站
dp.get(
    'https://www.zhipin.com/web/geek/jobs?city=100010000&position=100101,100102,100103,100109,100106,100107,100116,100114,100125,100124,101313,100121,100123,100608,100199,100901,100213,100202,100203,100209,100211,100210,100212,100308,100305,100303,100302,100310,100703,100301,100307,100304,100309,100401,100405,100403,100407,100404,100408,290166,100409,100406,100402,100410,101306,101312,100117,100118,100115,101310,101305,100104,101311,101309,101302,101301,101307,100120,101308,130121,101201,100511,100514,101202,100508,100122,100507,101299,160303,100506,100515,100512,100607,100605,100606,100601,100603,100701,100704,100702,100705,100707,100706'
)
#循环翻页
for page in range(1,21):
    print(f'正在采集第{page}页的内容')
    # 等待数据包加载
    resp = dp.listen.wait()
    # 获取数据
    json_data = resp.response.body

    # 字典取值：提供职位相关信息所在的列表
    jobList = json_data['zpData']['jobList']
    # for循环遍历，提取列表中的元素
    for job in jobList:
        dit = {
            '职位': job['jobName'],
            '学历': job['jobDegree'],
            '经验': job['jobExperience'],
            '薪资': job['salaryDesc'],
            '所需技能': ''.join(job['skills']),
            '城市': job['cityName'],
            '区域': job['areaDistrict'],
            '商业区': job['businessDistrict'],
            '经度': job['gps']['longitude'],
            '纬度': job['gps']['latitude'],
            '公司': job['brandName'],
            '领域': job['brandIndustry'],
            '规模': job['brandScaleName'],
            '性质': job['brandStageName'],
            '福利': ''.join(job['welfareList']),
        }

        # 写入数据
        csv_writer.writerow(dit)
        print(dit)
    #下滑页面
    dp.scroll.to_bottom()


