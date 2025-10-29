
# Study & Learn v6.1 Hybrid（OpenAI対応版）

このZIPは**完全UI版（Streamlit）**です。WindowsでもmacOSでも動きます。  
ハイブリッド設計：**Local Only**（オフライン動作） / **OpenAI Hybrid**（API連携）をワンタップ切替。

## すぐに始める（Windows）
1. Python 3.10–3.12 をインストール済みであることを確認（推奨: 3.12）。
2. ZIP を任意のフォルダに展開（例: `C:\Users\owner\OneDrive\ドキュメント\study_learn_v61_hybrid`）。
3. フォルダ内で `start_app.bat` をダブルクリック。初回は必要なパッケージを自動で入れます。  
4. ブラウザが自動起動しない場合は、表示された URL（通常 `http://localhost:8501`）を開いてください。

## すぐに始める（macOS）
1. Python 3.10–3.12 をインストール。
2. ターミナルでこのフォルダに移動して `chmod +x start_app.command` を実行（初回のみ）。
3. Finder から `start_app.command` をダブルクリック。

## OpenAI を使う（Hybrid）
1. 画面左の **設定 ▶ APIキー** からキーを入力し保存。  
   - または `.env` に `OPENAI_API_KEY=sk-...` を記述。
2. サイドバーの「実行モード」で **OpenAI Hybrid** を選択。

## 主な機能
- **単語帳**：意味・コロケーション・例文・イメージ・IPA(発音記号)で管理。CSV出力/取込対応。
- **クイズ / 復習（SRS）**：到達度に応じた出題。復習タイミングはSM-2風の簡易実装。
- **文法コーチ / 英作文チェック**：ローカル簡易診断 or OpenAIで高精度解説（日本語/英語切替）。
- **発音ヒント**：IPA表示・音素の要点メモ。TTSは任意（環境ごと）。
- **ダークテーマ対応**。

## フォルダ構成
```
study_learn_v61_hybrid/
├─ streamlit_app.py
├─ requirements.txt
├─ start_app.bat / start_app.command
├─ .env.example
├─ .streamlit/config.toml
└─ study/
   ├─ data/
   │  ├─ vocab_seed.csv
   │  └─ grammar_seed.json
   └─ utils/
      ├─ openai_client.py
      ├─ srs.py
      ├─ storage.py
      ├─ ui.py
      └─ ipa.py
```

## よくある質問
- **app.py をダブルクリックしても一瞬で閉じる**  
  → `start_app.bat` / `start_app.command` を使ってください。ログが見えます。
- **ポート競合（8501）がある**  
  → 自動で次のポートに切り替えます。うまくいかない場合は `--server.port 8505` などに変更可。
- **日本語フォント崩れ**  
  → ブラウザのズームを100%に。必要ならブラウザを再起動。

Happy learning! 🎉
