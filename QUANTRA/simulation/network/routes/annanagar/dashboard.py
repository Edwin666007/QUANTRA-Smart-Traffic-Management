import streamlit as st
from streamlit_lottie import st_lottie
import traci
import os
import sys
import time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
st.set_page_config(page_title="QUANTRA: Intelligent City Twin", layout="wide", page_icon="⚛️")
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Headers - Gold & Glowing */
    h1, h2, h3 { 
        color: #FFD700 !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5);
    }
    
    /* Metrics Box Design */
    div[data-testid="stMetric"] {
        background-color: #111111;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stMetricLabel { color: #888 !important; font-size: 14px !important; }
    .stMetricValue { color: #fff !important; font-size: 28px !important; font-weight: bold !important; }

    /* Button Styling */
    .stButton>button {
        color: #000;
        background-color: #FFD700;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #e6c200;
        box-shadow: 0px 0px 15px #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_city = load_lottieurl("https://lottie.host/5a8e77c4-0b73-4556-9467-5d27299a4660/8s6y8Z3s6r.json") # Example City Animation
lottie_quantum = load_lottieurl("https://lottie.host/96057207-657c-473d-88b1-389f41088713/Gq6Z7I0V7h.json") # Tech Chip Animation


simulator = AerSimulator()

def get_quantum_decision(car_count):
    if car_count < 5: return False, 0
    qc = QuantumCircuit(1, 1)
    theta = (car_count / 25) * np.pi 
    qc.ry(theta, 0) 
    qc.measure(0, 0)
    job = simulator.run(transpile(qc, simulator), shots=1)
    result = job.result().get_counts()
    prob = int((theta / np.pi) * 100)
    return '1' in result, prob

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103650.png", width=80)
    st.title("🎛️ SYSTEM CONTROL")
    st.markdown("---")
    status_text = st.empty()
    run_simulation = st.button("🚀 INITIATE SYSTEM", use_container_width=True)
    st.markdown("---")
    st.markdown("**Core Status:** `ONLINE`")
    st.markdown("**Algorithm:** `QAOA Hybrid`")
    if lottie_quantum:
        st_lottie(lottie_quantum, height=150, key="quantum_anim")

col_title, col_anim = st.columns([3, 1])
with col_title:
    st.title("QUANTRA")
    st.markdown("### 🏙️ Urban Digital Twin & Quantum Traffic Orchestrator")
with col_anim:
    if lottie_city:
        st_lottie(lottie_city, height=120, key="city_anim")

# Metrics Row
m1, m2, m3, m4 = st.columns(4)
metric_cars = m1.empty()
metric_phase = m2.empty()
metric_qload = m3.empty()
metric_status = m4.empty()

# Initialize Metrics
metric_cars.metric("🚗 Waiting Vehicles", "0")
metric_phase.metric("🚦 Signal Phase", "Phase 0")
metric_qload.metric("⚛️ Quantum Probability", "0%")
metric_status.metric("⚡ System State", "IDLE")

st.markdown("---")

g1, g2 = st.columns([2, 1])

with g1:
    st.subheader("📈 Real-Time Density Analysis")
    chart_placeholder = st.empty()

with g2:
    st.subheader("📜 Quantum Execution Logs")
    log_box = st.empty()

if run_simulation:
    status_text.success("System Running...")
    
    # SUMO Connect
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        os.environ['SUMO_HOME'] = r"C:\Program Files (x86)\Eclipse\Sumo"
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)

    sumoBinary = r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo-gui.exe"
    if not os.path.exists(sumoBinary):
         sumoBinary = r"C:\Program Files\Eclipse\Sumo\bin\sumo-gui.exe"
         
    sumoCmd = [sumoBinary, "-c", "osm.sumocfg", "--start"]

    try:
        traci.start(sumoCmd)
    except:
        try:
            traci.close()
            traci.start(sumoCmd)
        except:
             st.error("Could not connect to SUMO. Is it already open?")
             sys.exit()

    traffic_lights = traci.trafficlight.getIDList()
    if not traffic_lights:
        st.error("No Traffic Lights found in Map!")
        sys.exit()
        
    target_junction = traffic_lights[0]
    lanes = traci.trafficlight.getControlledLanes(target_junction)
    
    step = 0
    current_phase = 0
    data_points = []
    logs = []

    while step < 1000:
        traci.simulationStep()
        step += 1
        
        if step % 5 == 0:
            # 1. Get Data
            total_waiting = 0
            for lane in lanes:
                total_waiting += traci.lane.getLastStepHaltingNumber(lane)

            # 2. Quantum Decision
            triggered, prob = get_quantum_decision(total_waiting)
            
            # 3. Action
            state_msg = "MONITORING"
            if triggered:
                current_phase = (current_phase + 1) % 4
                traci.trafficlight.setPhase(target_junction, current_phase)
                state_msg = "OPTIMIZING"
                logs.append(f"⏱️ Step {step}: High Load ({total_waiting}) ➔ PHASE SWITCH ➔ {current_phase}")
            
            # 4. Update UI
            metric_cars.metric("🚗 Waiting Vehicles", f"{total_waiting}")
            metric_phase.metric("🚦 Signal Phase", f"Phase {current_phase}")
            metric_qload.metric("⚛️ Quantum Probability", f"{prob}%")
            metric_status.metric("⚡ System State", state_msg)
            
            # 5. Professional Plotly Chart (Neon Style)
            data_points.append(total_waiting)
            df = pd.DataFrame(data_points, columns=["Density"])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=df["Density"],
                mode='lines',
                name='Traffic Density',
                line=dict(color='#FFD700', width=3), # Gold Line
                fill='tozeroy',
                fillcolor='rgba(255, 215, 0, 0.1)' # Gold Glow
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                margin=dict(l=0, r=0, t=0, b=0),
                height=300,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#333')
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True)

            log_text = ""
            for log in reversed(logs[-6:]):
                log_text += f"> {log}\n"
            if not log_text: log_text = "> System Initialized. Waiting for traffic..."
            log_box.code(log_text, language="bash")

            time.sleep(0.05) 
        
    traci.close()