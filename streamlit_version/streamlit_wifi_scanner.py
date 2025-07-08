import streamlit as st
import pywifi
from pywifi import const
import pandas as pd
import time
import os

# ---------- Cloud Detection ----------
def is_cloud():
    return os.getenv("HOME") == "/home/app"

# ---------- Wi-Fi SCAN Functions ----------
def akm_type_to_string(akm_type):
    mapping = {
        const.AKM_TYPE_NONE: "Open",
        const.AKM_TYPE_WPA: "WPA",
        const.AKM_TYPE_WPAPSK: "WPA-PSK",
        const.AKM_TYPE_WPA2: "WPA2",
        const.AKM_TYPE_WPA2PSK: "WPA2-PSK",
        const.AKM_TYPE_UNKNOWN: "Unknown"
    }
    return mapping.get(akm_type, "Other")

def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(3)
    results = iface.scan_results()

    networks = []
    for network in results:
        ssid = network.ssid
        signal = f"{network.signal} dBm"
        security = akm_type_to_string(network.akm[0]) if network.akm else "Open"
        networks.append({"SSID": ssid, "Signal": signal, "Security": security})

    return pd.DataFrame(networks)

# ---------- STREAMLIT UI ----------

st.set_page_config("Wi-Fi Scanner", layout="centered")
st.title("📶 Wi-Fi Network Scanner")
st.write("Scan nearby Wi-Fi networks and view signal strength and security type.")

# Store scan results in session
if 'wifi_data' not in st.session_state:
    st.session_state.wifi_data = pd.DataFrame()

# Mode selection
mode = st.radio("Select Mode", ["Live Mode", "Demo Mode"])

# Show warning if cloud
if is_cloud():
    st.warning("⚠️ Live scanning is disabled on Streamlit Cloud.\nYou're now in Demo Mode.")

# STEP 1: Scan button
if st.button("🔍 Find Networks"):
    try:
        if mode == "Demo Mode" or is_cloud():
            df = pd.DataFrame([
                {"SSID": "CU_WiFi", "Signal": "-45 dBm 🟩🟩🟩🟩🟩", "Security": "WPA2"},
                {"SSID": "Public_WiFi", "Signal": "-80 dBm 🟥🟥", "Security": "Open ⭐"}
            ])
        else:
            df = scan_wifi()
        st.session_state.wifi_data = df
        st.success("✅ Scan complete! Scroll down to view results.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# STEP 2: Show results + Refresh + Download
if not st.session_state.wifi_data.empty:
    st.subheader("📋 Available Wi-Fi Networks")
    st.dataframe(st.session_state.wifi_data)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔁 Refresh"):
            try:
                if mode == "Demo Mode" or is_cloud():
                    df = pd.DataFrame([
                        {"SSID": "CU_WiFi", "Signal": "-45 dBm 🟩🟩🟩🟩🟩", "Security": "WPA2"},
                        {"SSID": "Public_WiFi", "Signal": "-80 dBm 🟥🟥", "Security": "Open ⭐"}
                    ])
                else:
                    df = scan_wifi()
                st.session_state.wifi_data = df
                st.success("✅ Data refreshed!")
            except Exception as e:
                st.error(f"❌ Refresh failed: {e}")

    with col2:
        csv = st.session_state.wifi_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="wifi_networks.csv",
            mime="text/csv"
        )

# STEP 3: Clear button
if not st.session_state.wifi_data.empty:
    if st.button("🗑️ Clear Results"):
        st.session_state.wifi_data = pd.DataFrame()
        st.info("Wi-Fi data cleared. You can scan again.")
