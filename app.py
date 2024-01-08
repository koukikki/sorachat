
import streamlit as st
import openai
from PIL import Image

image = Image.open('favicon.png')
st.set_page_config(
    page_title="Sora Chat",
    page_icon=image,
    menu_items={
         'About': """
         # Sora Chat
         私の飼い猫の空の生態を答えるチャットボットです。
         """
     })

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは飼い猫の「空」の飼い主で生態や特徴を説明します。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal::8MxtO1v6",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# メッセージを表示するための関数
def display_message(message):
    if message["role"] == "assistant":
        # アシスタントのメッセージは左寄り
        st.markdown(f"<p style='text-align: left;'>🤖: {message['content']}</p>", unsafe_allow_html=True)
    else:
        # ユーザーのメッセージは右寄り
        st.markdown(f"<p style='text-align: right;'>{message['content']} : 🙂</p>", unsafe_allow_html=True)

# ユーザーインターフェイスの構築
st.title("Sora Chat")
st.write("愛猫🐈の空の生態を答えるチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        display_message(message)
