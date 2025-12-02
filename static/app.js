let ws;
let isRunning = false;

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === 'telemetry') {
            updateInstruments(msg.data);
            updateLogs(msg.errors);
        } else if (msg.type === 'status') {
            logSystemMessage(msg.message);
            if (msg.message === "Simulation Completed") {
                setRunningState(false);
            }
        }
    };

    ws.onclose = () => {
        console.log("WebSocket disconnected");
    };
}

function updateInstruments(data) {
    document.getElementById('altitude').innerText = data.altitude;
    document.getElementById('airspeed').innerText = data.airspeed;
    document.getElementById('flaps').innerText = data.flaps_setting;
    
    const gearEl = document.getElementById('gear');
    gearEl.innerText = data.landing_gear_state ? "DOWN" : "UP";
    gearEl.style.color = data.landing_gear_state ? "#4caf50" : "#f44336";
}

function updateLogs(errors) {
    const logList = document.getElementById('logList');
    // Clear existing logs to avoid duplicates if re-sending full list, 
    // but for now we append new ones. Ideally backend sends only new ones.
    // The backend logic sends ALL errors every time for simplicity in the prototype.
    // So we clear and rebuild.
    logList.innerHTML = '';
    
    errors.forEach(err => {
        const div = document.createElement('div');
        div.className = 'log-entry';
        div.innerText = `[${err.timestamp.toFixed(1)}] ${err.rule_id}: ${err.details}`;
        logList.appendChild(div);
    });
    
    // Scroll to bottom
    logList.scrollTop = logList.scrollHeight;
}

async function startSimulation() {
    if (isRunning) return;
    
    try {
        await fetch('/api/start', { method: 'POST' });
        setRunningState(true);
        logSystemMessage("Simulation Started");
    } catch (e) {
        console.error(e);
    }
}

async function stopSimulation() {
    if (!isRunning) return;

    try {
        await fetch('/api/stop', { method: 'POST' });
        setRunningState(false);
        logSystemMessage("Simulation Stopped");
    } catch (e) {
        console.error(e);
    }
}

function setRunningState(running) {
    isRunning = running;
    document.getElementById('startBtn').disabled = running;
    document.getElementById('stopBtn').disabled = !running;
}

async function sendChat() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;

    addChatMessage(message, 'user');
    input.value = '';

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await res.json();
        addChatMessage(data.response, 'bot');
    } catch (e) {
        addChatMessage("Error connecting to FCA.", 'system');
    }
}

function addChatMessage(text, sender) {
    const history = document.getElementById('chatHistory');
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.innerText = text;
    history.appendChild(div);
    history.scrollTop = history.scrollHeight;
}

function handleChatKey(e) {
    if (e.key === 'Enter') sendChat();
}

function logSystemMessage(text) {
    const logList = document.getElementById('logList');
    const div = document.createElement('div');
    div.style.color = '#b2b2b2';
    div.style.padding = '5px';
    div.innerText = `[SYSTEM] ${text}`;
    logList.appendChild(div);
    logList.scrollTop = logList.scrollHeight;
}

// Init
connectWebSocket();
