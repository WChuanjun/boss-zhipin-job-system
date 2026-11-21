from flask import Flask, jsonify
from flask_cors import CORS
from visual import chart_map
from ai_predict import match_job

from load_data import get_df
df = get_df()

app = Flask(__name__)
CORS(app)

@app.route("/api/chart/<chart_name>")
def get_chart(chart_name):
    chart = chart_map.get(chart_name)
    if chart is None:
        return "chart not found", 404
    return chart.render_embed()


@app.route("/all")
def all_charts():
    c_city = chart_map["city"].render_embed()
    c_edu_sal = chart_map["edu_sal"].render_embed()
    c_exp = chart_map["exp"].render_embed()
    c_edu_pie = chart_map["edu_pie"].render_embed()
    c_scale_pie = chart_map["scale_pie"].render_embed()
    c_wordcloud = chart_map["wordcloud"].render_embed()

    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>BOSS直聘岗位数据分析</title>
        <style>
            body {{padding:20px; background:#f5f7fa;}}
            h2 {{text-align:center}}
            .row {{display:flex; gap:20px; margin-bottom:20px;}}
            .item {{flex:1; background:#fff; padding:15px; border-radius:8px; box-shadow:0 2px 8px #00000015;}}
            .ai-box {{background:#fff; padding:20px; border-radius:8px; box-shadow:0 2px 8px #00000015; margin-top:30px;}}
            .form-line {{margin:10px 0;}}
            input,select {{padding:6px; width:200px; margin-right:10px;}}
            button {{padding:7px 16px; background:#2385bb; color:#fff; border:none; border-radius:4px; cursor:pointer;}}
            #result {{margin-top:15px;}}
            .job-item {{border:1px solid #eee; padding:10px; margin:8px 0; border-radius:6px;}}
        </style>
    </head>
    <body>
        <h2>BOSS直聘岗位数据分析可视化 + AI岗位匹配</h2>

        <div class="row">
            <div class="item">{c_city}</div>
            <div class="item">{c_edu_sal}</div>
        </div>
        <div class="row">
            <div class="item">{c_exp}</div>
            <div class="item">{c_edu_pie}</div>
        </div>
        <div class="row">
            <div class="item">{c_scale_pie}</div>
            <div class="item">{c_wordcloud}</div>
        </div>

        <div class="ai-box">
            <h3>智能岗位匹配查询</h3>
            <div class="form-line">
                <label>技能关键词：</label>
                <input id="skill" placeholder="例如 Java MySQL" value="">
            </div>
            <div class="form-line">
                <label>学历：</label>
                <select id="edu">
                    <option value="学历不限">学历不限</option>
                    <option value="大专">大专</option>
                    <option value="本科">本科</option>
                    <option value="硕士">硕士</option>
                </select>
                <label>工作经验：</label>
                <select id="exp">
                    <option value="经验不限">经验不限</option>
                    <option value="应届生">应届生</option>
                    <option value="1-3年">1-3年</option>
                    <option value="3-5年">3-5年</option>
                </select>
            </div>
            <div class="form-line">
                <label>薪资下限：</label>
                <input id="sal_min" type="number" value="0">
                <label>薪资上限：</label>
                <input id="sal_max" type="number" value="999">
            </div>
            <button onclick="searchJob()">开始匹配</button>
            <div id="result"></div>
        </div>

        <script>
            function searchJob(){{
                let skill = document.getElementById('skill').value;
                let edu = document.getElementById('edu').value;
                let exp = document.getElementById('exp').value;
                let sal_min = document.getElementById('sal_min').value;
                let sal_max = document.getElementById('sal_max').value;
                let url = `/api/recommend?skill=${{skill}}&edu=${{edu}}&exp=${{exp}}&sal_min=${{sal_min}}&sal_max=${{sal_max}}`
                fetch(url).then(res=>res.json()).then(data=>{{
                    let html = "";
                    if(data.length === 0){{
                        html = "<p>没有匹配到岗位</p>";
                    }}else{{
                        for(let item of data){{
                            html += `
                            <div class="job-item">
                                <b>${{item.岗位名称}}</b> | ${{item.公司}} | ${{item.城市}} <br>
                                学历：${{item.学历}} | 经验：${{item.工作经验}} | 薪资：${{item.薪资}} <br>
                                技能：${{item.技能}} | 匹配分：${{item.匹配分数}}
                            </div>
                            `
                        }}
                    }}
                    document.getElementById('result').innerHTML = html;
                }})
            }}
        </script>
    </body>
    </html>
    """
    return html


@app.route("/api/recommend")
def recommend():
    import flask
    skill = flask.request.args.get("skill", "")
    edu = flask.request.args.get("edu", "学历不限")
    exp = flask.request.args.get("exp", "经验不限")
    sal_min = float(flask.request.args.get("sal_min", 0))
    sal_max = float(flask.request.args.get("sal_max", 999))
    res = match_job(skill, edu, exp, sal_min, sal_max)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
