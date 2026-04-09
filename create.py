import streamlit as st
import numpy as np
import pickle
import time
import pandas as pd

st.write("App is running...")

# ✅ Safe loading
try:
    model = pickle.load(open("model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
except:
    st.error("❌ model.pkl or scaler.pkl not found. Please check files.")
    st.stop()

st.title("🛡️ AI Network Intrusion Detection System")

st.write("Click the button to analyze network traffic")

# ✅ AI Explanation
def explain_attack(prob):
    if prob > 0.8:
        return "🔥 High probability of DDoS attack due to abnormal traffic"
    elif prob > 0.5:
        return "⚠️ Suspicious activity detected (possible probing)"
    else:
        return "✅ Traffic appears normal"

# ✅ Attack Type
def attack_type(prob):
    if prob > 0.8:
        return "DDoS Attack"
    elif prob > 0.6:
        return "Probe Attack"
    elif prob > 0.4:
        return "Brute Force Attempt"
    else:
        return "Normal Traffic"

# ✅ Session storage
if "history" not in st.session_state:
    st.session_state.history = []

if "alerts" not in st.session_state:
    st.session_state.alerts = 0

# ✅ BUTTON
if st.button("Analyze Traffic"):

    sample = np.random.rand(scaler.n_features_in_).reshape(1, -1)
    sample_scaled = scaler.transform(sample)

    prediction = model.predict(sample_scaled)[0]
    prob = model.predict_proba(sample_scaled)[0][1]
    risk = round(prob * 100, 2)

    # Save history
    st.session_state.history.append(risk)

    # Count alerts
    if prediction == 1:
        st.session_state.alerts += 1

    # 🔴🟢 Status
    if prediction == 1:
        st.error(f"🚨 Attack Detected")
        st.markdown("### 🔴 Status: UNDER ATTACK")
    else:
        st.success("✅ Normal Traffic")
        st.markdown("### 🟢 Status: SAFE")

    # 📊 Risk Meter
    st.write("### 📊 Risk Level")
    st.progress(risk / 100)
    st.write(f"Risk Score: {risk}%")

    # 🎯 Attack Type
    st.write("### 🎯 Attack Type")
    st.write(attack_type(prob))

    # 🧠 AI Explanation
    st.write("### 🧠 AI Analysis")
    st.write(explain_attack(prob))

    # 📊 Sample Data
    st.write("### 📊 Sample Traffic Data (first 10 features)")
    st.write(sample[0][:10])

# 📈 Live Graph
st.write("### 📈 Live Risk Trend")
if len(st.session_state.history) > 0:
    df = pd.DataFrame(st.session_state.history, columns=["Risk"])
    st.line_chart(df)

# 🚨 Alert Counter
st.write(f"🚨 Total Alerts: {st.session_state.alerts}")

# 📜 Logs
st.write("### 📜 Detection Logs")
st.write(st.session_state.history)

# 🔄 Auto Refresh
if st.checkbox("Enable Live Monitoring"):
    time.sleep(2)
    st.rerun()