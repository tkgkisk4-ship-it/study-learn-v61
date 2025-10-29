# 📱 Mobile Deploy Kit — Study & Learn v6.1 Hybrid

このキットで、スマホ（iOS/Android）から使えるURLに簡単デプロイできます。既存ZIPと同じフォルダに**追加**して使ってください。

## 道① Hugging Face Spaces（無料・お手軽）
1. GitHubに `study_learn_v61_hybrid` をプッシュ、またはSpaceで**Upload files**。
2. 新規Space → **Streamlit** を選択。
3. `app.py`、`streamlit_app.py`、`requirements.txt`、`.streamlit/config.toml` をアップロード。
4. **Secrets** に `OPENAI_API_KEY` を設定（Hybrid利用時）。
5. ビルド完了後のURLをスマホで開く → **「ホーム画面に追加」**で擬似アプリ化。

## 道② Render（無料ティア有）
- このキットに含まれる `Procfile` と `render.yaml` あり。
1. 新規 **Web Service** → リポジトリを接続。
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
4. 環境変数に `OPENAI_API_KEY` を設定（必要なら）。
5. デプロイ完了のURLをスマホからアクセス。

## 道③ Railway（無料ティア有）
- `railway.json` を参考にデプロイ。
- Start Command は Render と同様。

## 道④ 自宅PCで動かしてスマホから使う（トンネリング）
**ローカルPCで動作** → 外部URLを発行してスマホからアクセス。  
例：**Cloudflare Tunnel**（無料）
```bash
# アプリ起動（PC）
streamlit run streamlit_app.py --server.port 8501

# べつのターミナルで（Cloudflareアカウント必要）
cloudflared tunnel --url http://localhost:8501
```
発行URLをスマホで開けばOK。OpenAIキーはPC側の環境変数か `.env` を使用。

---
### スマホで快適に使うコツ
- iOS/Androidともにブラウザのメニューから**「ホーム画面に追加」**すると、擬似ネイティブアプリに。
- Streamlitはモバイル対応済み。入力欄が小さい場合は画面のズームまたは端末の表示サイズを調整。
- 長文入力は「英作文チェック」タブのテキストエリアを活用。

### セキュリティ
- APIキーはリポジトリに入れず、**プラットフォームのSecrets/環境変数**を使用。
- 公開URLではデータが他ユーザに見えないように、必要なら**認証**（SpacesのPrivate/Org、Render Basic Authなど）を利用。

Good luck & happy mobile learning! 🚀
