
import streamlit as st

def sidebar_mode_key():
    return "run_mode"

def mode_selector():
    st.sidebar.subheader("実行モード")
    mode = st.sidebar.radio(
        "Local Only（オフライン）/ OpenAI Hybrid",
        options=["Local Only", "OpenAI Hybrid"],
        index=0,
        key=sidebar_mode_key()
    )
    return mode

def api_key_input():
    st.sidebar.subheader("設定 ▶ APIキー")
    with st.sidebar.expander("OpenAI APIキー", expanded=False):
        val = st.text_input("OPENAI_API_KEY", type="password", key="api_input")
        if st.button("保存／更新"):
            st.session_state["OPENAI_API_KEY"] = val
            st.success("APIキーをセッションに保存しました。")
        st.caption("※ 永続保存は .env を使用してください（README参照）。")

def top_nav():
    return st.tabs(["🏠 ホーム","📘 単語帳","🧠 クイズ/復習","📝 文法コーチ","✍️ 英作文チェック","🔊 発音ヒント","⚙️ ツール"])
