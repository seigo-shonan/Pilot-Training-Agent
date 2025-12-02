import json
import time
from models import AircraftState

def generate_mock_data(filename="mock_flight_data.json"):
    data = []
    start_time = time.time()
    
    # Simulate a takeoff sequence
    for i in range(60):
        state = AircraftState(
            timestamp=start_time + i,
            altitude=100 + i * 10,
            airspeed=80 + i * 2,
            engine_power_setting=95.0,
            flaps_setting=10 if i < 30 else 0,
            landing_gear_state=True if i < 20 else False,
            checklist_status="Takeoff_Config_OK" if i < 10 else "In_Flight"
        )
        data.append(state.__dict__)
        
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Generated {len(data)} records to {filename}")

if __name__ == "__main__":
    generate_mock_data()
