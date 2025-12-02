# ✈️ Pilot Training Agent System (AIパイロット訓練システム)

## 📖 概要 (Overview)
マルチエージェント・アーキテクチャを活用し、パイロットの飛行訓練におけるPDCAサイクル（実行・評価・改善）を自律的に自動化するシステムです。
フライトシミュレーターそのものではなく、「AI教官（インストラクター）」としてのバックエンドロジックを実装しています。

## 🤖 アーキテクチャ (Agents)
このシステムは3つの自律エージェントにより構成されています。

1. **PEA (Performance Evaluation Agent)**: リアルタイム監視とSOP違反の評価
2. **SGA (Scenario Generation Agent)**: 弱点分析と適応型シナリオ（トラブル注入など）の生成
3. **FCA (Feedback Coaching Agent)**: 訓練生への対話的コーチング

## 🚀 特徴 (Features)
* **Stateful Learning**: JSONファイルによるデータ永続化により、システムを再起動しても前回の学習状況を引き継ぎます。
* **Adaptive Injection**: 苦手な操作（ギア、フラップ等）に応じて、センサー故障や悪天候などのトラブルを自動的にシナリオに注入します。

## 🛠 使い方 (How to Run)

### 前提条件
* Python 3.8以上

### 実行手順
1. リポジトリをクローン:
   ```bash
   git clone [https://github.com/あなたのID/pilot-training-agent.git](https://github.com/あなたのID/pilot-training-agent.git)
