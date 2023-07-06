import streamlit as st
import requests
import datetime

st.title("OpenAI 计费信息查询")

# 输入API Key
apikey = st.text_input("请输入您的OpenAI API Key：")

# 点击查询按钮
if st.button("查询"):
    # 设置请求头
    headers = {"Authorization": "Bearer " + apikey, "Content-Type": "application/json"}

    # 请求订阅信息
    subscription_url = "https://service-6ehx9pyq-1317411446.usw.apigw.tencentcs.com/v1/dashboard/billing/subscription"
    subscription_response = requests.get(subscription_url, headers=headers)

    # 判断请求是否成功
    if subscription_response.status_code == 200:
        data = subscription_response.json()
        total = data.get("hard_limit_usd")
    else:
        st.error(subscription_response.text)
        st.stop()

    # 设置查询日期范围
    start_date = (datetime.datetime.now() - datetime.timedelta(days=99)).strftime(
        "%Y-%m-%d"
    )
    end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )

    # 请求计费信息
    billing_url = f"https://service-6ehx9pyq-1317411446.usw.apigw.tencentcs.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"
    billing_response = requests.get(billing_url, headers=headers)

    # 判断请求是否成功
    if billing_response.status_code == 200:
        data = billing_response.json()
        total_usage = data.get("total_usage") / 100
        daily_costs = data.get("daily_costs")
        days = min(5, len(daily_costs))
        recent = f"最近{days}天使用情况  \n"
        for i in range(days):
            cur = daily_costs[-i - 1]
            date = datetime.datetime.fromtimestamp(cur.get("timestamp")).strftime(
                "%Y-%m-%d"
            )
            line_items = cur.get("line_items")
            cost = 0
            for item in line_items:
                cost += item.get("cost")
            recent += f"\t{date}\t{cost / 100} \n"
    else:
        st.error(billing_response.text)
        st.stop()

    # 显示查询结果
    st.write(
        f"\n总额:\t{total:.4f}  \n"
        f"已用:\t{total_usage:.4f}  \n"
        f"剩余:\t{total-total_usage:.4f}  \n"
        f"\n" + recent
    )
