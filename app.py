import streamlit as st
import main
import json
import pandas as pd  # データ分析用ライブラリ

st.set_page_config(page_title="AI Pilot Trainer", layout="wide") # 画面を広く使う

st.title("✈️ AI Pilot Training System")
st.markdown("### 自律型エージェントによる適応型訓練シミュレーター")

# 2カラムに分ける（左：操作、右：ステータス）
col1, col2 = st.columns([1, 2])

with col1:
    st.info("システムの準備が完了しました。")
    # シミュレーション時間の調整スライダー
    duration = st.slider("訓練時間（分）", 1, 5, 1)
    
    if st.button("🚀 Start Simulation", type="primary"):
        with st.spinner("Agents are working... (PEA evaluating, SGA generating)"):
            # 実行
            main.run_training_session(duration)
        st.success("Training Cycle Complete!")

with col2:
    st.write("#### 📊 フライトデータ分析")
    
    # モックデータを読み込んでグラフ化する
    try:
        with open("mock_flight_data.json", "r") as f:
            data = json.load(f)
        
        # グラフ用にデータを変換
        df = pd.DataFrame(data)
        
       # （修正前）まとめて表示
        # st.line_chart(df[["altitude", "airspeed"]])
        
        # （修正後）2つのグラフに分けて表示
        st.write("📈 高度 (Altitude)")
        st.line_chart(df["altitude"], color="#00B4D8") # 水色
        
        st.write("🚀 速度 (Airspeed)")
        st.line_chart(df["airspeed"], color="#0077B6") # 濃い青
        
        st.write("#### ⚠️ 検出された違反 (PEA Report)")
        # エラーログの表示
        with open("PEA_Error_Log.json", "r") as f:
            errors = json.load(f)
        
        if errors:
            st.dataframe(errors) # 表形式で表示
        else:
            st.success("No violations detected. Good job!")
            
    except FileNotFoundError:
        st.warning("データファイルが見つかりません。一度シミュレーションを実行してください。")

# 下部にHTMLレポートを表示
st.write("---")
st.subheader("📝 最終フィードバックレポート")
try:
    with open("FeedbackReport.html", 'r') as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=400, scrolling=True)
except:
    st.caption("レポートはまだ生成されていません")
