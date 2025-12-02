import json
import random
import math
import os

def generate_mock_data(filename="mock_flight_data.json", duration_minutes=1):
    """
    SGAが生成したシナリオ設定を読み込み、それに基づいたフライトデータを生成する
    """
    
    # 1. SGAが作った設定ファイルがあれば読み込む
    scenario_conditions = {}
    injection_file = "ScenarioInjection.json"
    
    if os.path.exists(injection_file):
        try:
            with open(injection_file, 'r') as f:
                config = json.load(f)
                scenario_conditions = config.get("conditions", {})
                print(f"[Generator] Loaded Scenario Config: {scenario_conditions}")
        except:
            print("[Generator] Could not load scenario config. Using defaults.")
    else:
        print("[Generator] No scenario file found. Generating standard flight.")

    # 2. シナリオ条件の適用（パラメータ設定）
    # 風が強い設定なら、揺れ（ノイズ）を大きくする
    wind_factor = 0.5
    if scenario_conditions.get("wind_speed", 0) > 10:
        wind_factor = 5.0  # 揺れを10倍にする
    elif scenario_conditions.get("runway_condition") == "wet":
        wind_factor = 2.0

    # 3. 時系列データの生成
    data = []
    total_steps = int(duration_minutes * 60 * 2) # 0.5秒刻み
    
    # フライトフェーズのシミュレーション（離陸 -> 巡行 -> 着陸）
    current_alt = 0
    current_speed = 0
    gear_state = True # True=Down, False=Up
    flaps = 20
    
    for t in range(total_steps):
        # --- 単純な物理モデル ---
        
        # 前半は上昇（離陸）、後半は下降（着陸）
        if t < total_steps / 2:
            # 上昇フェーズ
            target_speed = 160
            target_alt = 2000
            phase = "CLIMB"
        else:
            # 下降フェーズ
            target_speed = 140
            target_alt = 0
            phase = "DESCENT"

        # 値の更新（徐々にターゲットに近づける）
        current_speed += (target_speed - current_speed) * 0.05
        current_alt += (target_alt - current_alt) * 0.05
        
        # ★ここで「シナリオ」による変化（ノイズ）を加える★
        # 風の影響で速度と高度がふらつく
        noise = random.uniform(-wind_factor, wind_factor)
        current_speed += noise
        current_alt += noise * 2

        # ギア操作（パイロットの操作を模倣）
        # 基本的には高度300ftを超えたら上げる、下回ったら下げる（優等生）
        # ただし、たまに「うっかりミス」を発生させる（デモ用）
        error_chance = 0.02 # 2%の確率で操作を忘れる（ここを変えるとミスの頻度が変わる）
        
        if random.random() > error_chance: 
            if current_alt > 300 and phase == "CLIMB":
                gear_state = False # Gear Up
                flaps = 0
            elif current_alt < 800 and phase == "DESCENT":
                gear_state = True # Gear Down
                flaps = 20
        
        # データの1行を作成
        state = {
            "timestamp": t,
            "altitude": max(0, round(current_alt, 2)), # マイナスにならないように
            "airspeed": max(0, round(current_speed, 2)),
            "vertical_speed": round(random.uniform(-500, 500) if phase=="CLIMB" else random.uniform(-800, 200), 2),
            "heading": 360,
            "landing_gear_state": gear_state,
            "flaps_setting": flaps
        }
        data.append(state)

    # 4. ファイルに保存
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"[Generator] Generated {len(data)} data points based on scenario.")

if __name__ == "__main__":
    generate_mock_data()
