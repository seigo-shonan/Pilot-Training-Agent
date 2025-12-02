import json
import time
import sys
# ↓ ここ重要！mock_data_generator から関数を読み込む記述が必要です
from mock_data_generator import generate_mock_data 
from models import AircraftState, SOPRule
from pea import PerformanceEvaluationAgent
from sga import ScenarioGenerationAgent
from fca import FeedbackCoachingAgent

# Define some basic SOP Rules
RULES = [
    SOPRule(
        rule_id="GEAR_CHECK",
        pre_condition="Altitude < 500ft",
        required_action="Landing Gear DOWN",
        time_limit_sec=10.0,
        severity=5
    ),
    SOPRule(
        rule_id="FLAPS_TAKEOFF",
        pre_condition="Altitude < 1000ft & Speed < 150kts",
        required_action="Flaps > 0",
        time_limit_sec=5.0,
        severity=4
    )
]

def load_mock_data(filename="mock_flight_data.json"):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        # Convert dicts back to AircraftState objects
        return [AircraftState(**d) for d in data]
    except FileNotFoundError:
        print("Mock data not found. Generating...")
        generate_mock_data(filename)
        return load_mock_data(filename)

def run_training_session(duration_minutes=1):
    print(f"Starting Training Session for {duration_minutes} minutes (simulated)...")
    
    # Initialize Agents
    pea = PerformanceEvaluationAgent()
    sga = ScenarioGenerationAgent()
    fca = FeedbackCoachingAgent(RULES)
    
    # Clear previous logs (optional)
    with open(pea.error_log_file, 'w') as f:
        json.dump([], f)

    # ★修正ポイント: 毎回新しいデータを生成してから読み込む★
    print("[System] Generating new scenario based on previous analysis...")
    generate_mock_data("mock_flight_data.json", duration_minutes)

    # Load Data
    flight_data = load_mock_data()
    
    # Real-time Monitoring Loop (Simulated)
    print("[System] Monitoring Loop Started...")
    
    # プログレスバーの表示（Streamlit用ではないですが、コンソールで見やすくするため）
    total_steps = len(flight_data)
    
    for i, state in enumerate(flight_data):
        # Simulate real-time data stream (少し速めに再生)
        time.sleep(0.01) 
        
        # PEA Monitoring
        pea.evaluate_sop(state, RULES)
        
        # Simulated FCA Interaction (Demo trigger)
        if i % 100 == 0 and i > 0: 
            # print(f"\n[Instructor] Asking FCA: 'What about gear?'")
            # print(f"[FCA] {fca.ask('gear')}\n")
            pass

    print("[System] Monitoring Loop Ended.")
    
    # Auto-adjustment Workflow
    print("\n[System] Initiating Post-Session Workflow...")
    
    # 1. PEA Report
    pea.generate_feedback_report()
    
    # 2. SGA Analysis
    weakness = sga.analyze_weakness()
    
    # 3. SGA Scenario Generation
    if weakness:
        print(f"[SGA] Weakness detected: {weakness}. Updating scenario...")
        sga.generate_next_scenario(weakness)
    else:
        print("[SGA] No significant weaknesses detected. Maintaining standard scenario.")

if __name__ == "__main__":
    # Allow running from command line with duration
    duration = 1
    if len(sys.argv) > 1:
        try:
            duration = float(sys.argv[1])
        except ValueError:
            pass
    
    run_training_session(duration)

