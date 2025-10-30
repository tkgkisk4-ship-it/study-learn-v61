
import os, io, json, datetime as dt
import pandas as pdhttps://github.com/tkgkisk4-ship-it/study-learn-v61/blob/main/study_learn_v61_hybrid/study_learn_v61_hybrid/streamlit_app.py
import streamlit as st
from dotenv import load_dotenv

from study.utils import ui as ui_utils
from study.utils.storage import load_vocab, save_vocab
from study.utils.srs import sm2, next_due_date
from study.utils.openai_client import grammar_feedback
from study.utils.ipa import hint as ipa_hint

# -------------- Setup --------------
st.set_page_config(page_title="Study & Learn v6.1 Hybrid", layout="wide")
load_dotenv()

# sidebar
mode = ui_utils.mode_selector()
ui_utils.api_key_input()

# Apply OPENAI_API_KEY from sidebar session to env (session-limited)
if "OPENAI_API_KEY" in st.session_state and st.session_state["OPENAI_API_KEY"]:
    os.environ["OPENAI_API_KEY"] = st.session_state["OPENAI_API_KEY"]

# -------------- Tabs --------------
tab_home, tab_vocab, tab_quiz, tab_grammar, tab_writing, tab_pron, tab_tools = ui_utils.top_nav()

# -------------- Data --------------
df = load_vocab()

with tab_home:
    st.title("Study & Learn v6.1 Hybrid")
    st.write("モード：**{}**".format(mode))
    st.success("ローカル機能は常に使えます。OpenAIキーを設定するとハイブリッドで高精度化します。")
    st.markdown("""
    **主なタブ**
    - 📘 **単語帳**：登録・編集・インポート/エクスポート
    - 🧠 **クイズ/復習**：SM-2風復習スケジュール
    - 📝 **文法コーチ**：文法の簡易チェック（Hybridで強化）
    - ✍️ **英作文チェック**：自由英作文の総合フィードバック
    - 🔊 **発音ヒント**：IPAや要点メモ
    """)

with tab_vocab:
    st.header("単語帳")
    st.caption("意味・コロケーション・例文・イメージ・IPA(発音記号)まで一括管理")

    # Add new word
    with st.expander("新規追加", expanded=False):
        c1,c2,c3 = st.columns(3)
        with c1:
            w = st.text_input("単語", key="new_w")
            ipa = st.text_input("IPA", key="new_ipa")
            deck = st.text_input("デッキ", value="core", key="new_deck")
        with c2:
            mean = st.text_input("意味（日本語）", key="new_mean")
            coll = st.text_input("コロケーション（;区切り）", key="new_coll")
        with c3:
            ex_en = st.text_input("例文（英）", key="new_ex_en")
            ex_ja = st.text_input("例文（和）", key="new_ex_ja")
            img = st.text_input("イメージヒント", key="new_img")
        if st.button("追加"):
            if w:
                new_row = {
                    "word": w, "ipa": ipa, "meaning_ja": mean, "collocations": coll,
                    "example_en": ex_en, "example_ja": ex_ja, "image_hint": img,
                    "deck": deck, "ease": 2.5, "interval_days": 0,
                    "due_date": dt.date.today().isoformat()
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_vocab(df)
                st.success(f"追加しました：{w}")
            else:
                st.error("単語は必須です。")

    st.dataframe(df, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("CSVにエクスポート"):
            path = save_vocab(df)
            st.download_button("ダウンロード（vocab_seed.csv）", data=open(path,"rb").read(), file_name="vocab_seed.csv")
    with c2:
        csv_file = st.file_uploader("CSVからインポート（列名はREADME準拠）", type=["csv"])
        if csv_file:
            new_df = pd.read_csv(csv_file)
            for col in df.columns:
                if col not in new_df.columns:
                    new_df[col] = None
            df = new_df[df.columns]
            save_vocab(df)
            st.success("インポートしました。")

with tab_quiz:
    st.header("クイズ / 復習")
    today = dt.date.today()
    due_df = df[df["due_date"] <= today]
    st.write(f"今日の復習カード：**{len(due_df)}**")

    if len(due_df) == 0:
        st.info("今日は復習カードはありません。単語帳に追加するか、明日また来ましょう。")
    else:
        for idx, row in due_df.iterrows():
            with st.expander(f"🃏 {row['word']}  /  {row['ipa']}", expanded=True):
                st.write(f"意味：{row['meaning_ja']}")
                st.write(f"例文（英）：{row['example_en']}")
                st.write(f"例文（和）：{row['example_ja']}")
                st.write(f"コロケーション：{row['collocations']}")
                st.write(f"イメージ：{row['image_hint']}")

                q = st.radio("出来栄え（0=全く× ～ 5=余裕）", options=[0,1,2,3,4,5], horizontal=True, key=f"q_{idx}")
                if st.button("記録", key=f"save_{idx}"):
                    new_ease, new_interval = sm2(row["ease"] if pd.notna(row["ease"]) else 2.5,
                                                 int(q),
                                                 int(row["interval_days"]) if pd.notna(row["interval_days"]) else 0)
                    df.loc[idx, "ease"] = new_ease
                    df.loc[idx, "interval_days"] = new_interval
                    df.loc[idx, "due_date"] = next_due_date(new_interval)
                    save_vocab(df)
                    st.success(f"次回 {df.loc[idx,'due_date']} に復習します。")

with tab_grammar:
    st.header("文法コーチ")
    st.caption("Hybridを選ぶとOpenAIで高精度解析。Local Onlyは簡易チェック。")
    text = st.text_area("英文を入力してください", height=150, key="grammar_text")
    colA, colB = st.columns(2)
    with colA:
        lang = st.selectbox("解説の言語", ["ja","en"], index=0)
    with colB:
        st.write(" ")
        go = st.button("チェック")

    if go and text.strip():
        if mode == "OpenAI Hybrid":
            res = grammar_feedback(text, lang=lang)
        else:
            res = grammar_feedback(text, lang=lang)  # function内でローカルにフォールバック
        st.markdown("**結果**")
        st.write(res)

with tab_writing:
    st.header("英作文チェック")
    st.caption("自由英作文の構成・文法・自然さを総合評価")
    essay = st.text_area("英作文を入力（複数段落OK）", height=200, key="essay_text")
    if st.button("評価する"):
        prompt = f"Please evaluate the following essay for grammar, clarity, and naturalness. Provide corrections and a short model answer.\n\n{essay}"
        if mode == "OpenAI Hybrid":
            res = grammar_feedback(prompt, lang="ja")
        else:
            res = grammar_feedback(prompt, lang="ja")
        st.write(res)

with tab_pron:
    st.header("発音ヒント（IPA）")
    w = st.text_input("単語", key="pron_word")
    if st.button("ヒント表示"):
        st.write("IPA:", ipa_hint(w) or "(未登録)")
        st.caption("※ 詳細な発音記号は今後の拡張で辞書連携予定。")

with tab_tools:
    st.header("ツール")
    st.write("- 今日の日付：", dt.date.today())
    st.write("- データ保存先：`study/data/vocab_seed.csv`")
    st.write("- テーマは `.streamlit/config.toml` で変更できます。")
    st.code(open('.streamlit/config.toml','r').read(), language="toml")
