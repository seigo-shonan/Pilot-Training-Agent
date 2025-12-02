from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os
import json
import asyncio

from models import AircraftState, SOPRule
from pea import PerformanceEvaluationAgent
from sga import ScenarioGenerationAgent
from fca import FeedbackCoachingAgent
from mock_data_generator import generate_mock_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static directory if it doesn't exist
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Agents
RULES = [
    SOPRule("GEAR_CHECK", "Altitude < 500ft", "Landing Gear DOWN", 10.0, 5),
    SOPRule("FLAPS_TAKEOFF", "Altitude < 1000ft & Speed < 150kts", "Flaps > 0", 5.0, 4)
]
pea = PerformanceEvaluationAgent()
sga = ScenarioGenerationAgent()
fca = FeedbackCoachingAgent(RULES)

# Global State
simulation_running = False
flight_data = []
current_data_index = 0

class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    global flight_data
    # Ensure mock data exists
    generate_mock_data()
    with open("mock_flight_data.json", 'r') as f:
        data = json.load(f)
        flight_data = [AircraftState(**d) for d in data]

@app.post("/api/chat")
async def chat_with_fca(request: ChatRequest):
    response = fca.ask(request.message)
    return {"response": response}

@app.post("/api/start")
async def start_simulation():
    global simulation_running, current_data_index
    current_data_index = 0
    simulation_running = True
    return {"status": "started"}

@app.post("/api/stop")
async def stop_simulation():
    global simulation_running
    simulation_running = False
    return {"status": "stopped"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global simulation_running, flight_data, current_data_index
    
   # idx = 0
    try:
        while True:
            if simulation_running and current_data_index < len(flight_data):
                state = flight_data[current_data_index]
                
                # Run PEA
                # We need to capture PEA output. For now, let's just check the log file or modify PEA to return errors.
                # To keep it simple without rewriting PEA entirely, we will check if PEA adds to its log list.
                current_log_len = len(pea.error_log)
                pea.evaluate_sop(state, RULES)
                new_errors = pea.error_log[current_log_len:]
                
                payload = {
                    "type": "telemetry",
                    "data": state.__dict__,
                    "errors": new_errors
                }
                await websocket.send_json(payload)
                
                current_data_index += 1
                await asyncio.sleep(0.1) # 10Hz update rate
            elif current_data_index >= len(flight_data):
                # End of simulation
                simulation_running = False
                await websocket.send_json({"type": "status", "message": "Simulation Completed"})
                # Trigger SGA
                pea.generate_feedback_report()
                weakness = sga.analyze_weakness()
                if weakness:
                    sga.generate_next_scenario(weakness)
                current_data_index = 0 # Reset for next run
            else:
                await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print("Client disconnected")
