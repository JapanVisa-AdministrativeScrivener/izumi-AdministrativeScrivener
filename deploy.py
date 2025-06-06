from flask import Flask, render_template, request
import json

app = Flask(__name__)

# 在留資格の判定ルール
STATUS_RULES = {
    "エンジニア・専門職": [
        {"国籍": "日本"},
        {"年齢": {"min": 22}},
        {"学歴": ["大学卒業", "修士課程卒業"]},
        {"職歴": {"min": 3}},
        {"専門性": True}
    ],
    "技術・人文知識・国際業務": [
        {"国籍": "日本"},
        {"年齢": {"min": 22}},
        {"学歴": ["大学卒業", "修士課程卒業"]},
        {"職歴": {"min": 3}},
        {"専門性": True}
    ],
    "経営・管理": [
        {"国籍": "日本"},
        {"年齢": {"min": 25}},
        {"資本金": {"min": 5000000}},
        {"従業員数": {"min": 2}}
    ],
    "定住者": [
        {"在留年数": {"min": 10}},
        {"年齢": {"min": 20}}
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    data = request.form
    
    # 必要な情報の取得
    customer_info = {
        "国籍": data.get('nationality'),
        "年齢": int(data.get('age', 0)),
        "学歴": data.get('education'),
        "職歴": int(data.get('work_experience', 0)),
        "専門性": data.get('specialization') == 'yes',
        "資本金": int(data.get('capital', 0)),
        "従業員数": int(data.get('employees', 0)),
        "在留年数": int(data.get('residence_years', 0))
    }
    
    # 在留資格の判定
    recommended_status = []
    for status, rules in STATUS_RULES.items():
        if all(check_rule(customer_info, rule) for rule in rules):
            recommended_status.append(status)
    
    return render_template('result.html', 
                         recommended_status=recommended_status,
                         customer_info=customer_info)

def check_rule(customer_info, rule):
    for key, value in rule.items():
        if key == "国籍":
            if customer_info["国籍"] != value:
                return False
        elif key == "年齢":
            if customer_info["年齢"] < value["min"]:
                return False
        elif key == "学歴":
            if customer_info["学歴"] not in value:
                return False
        elif key == "職歴":
            if customer_info["職歴"] < value["min"]:
                return False
        elif key == "専門性":
            if customer_info["専門性"] != value:
                return False
        elif key == "資本金":
            if customer_info["資本金"] < value["min"]:
                return False
        elif key == "従業員数":
            if customer_info["従業員数"] < value["min"]:
                return False
        elif key == "在留年数":
            if customer_info["在留年数"] < value["min"]:
                return False
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
