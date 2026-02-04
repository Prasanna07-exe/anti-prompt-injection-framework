import streamlit as st
import requests

st.set_page_config(page_title="Secure GenAI Assistant")
st.title("🤖 Secure GenAI Assistant")

with st.form("chat_form", clear_on_submit=True):
    prompt = st.text_input("You:")
    submitted = st.form_submit_button("Send")

if submitted and prompt:
    res = requests.post(
        "http://127.0.0.1:8000/analyze",
        json={"prompt": prompt}
    ).json()

    st.markdown(f"**You:** {prompt}")

    if res["status"] == "blocked":
        st.error(f"⚠️ Blocked: {res['reason']}")
    else:
        st.success(res["response"])
