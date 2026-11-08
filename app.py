import streamlit as st
import pandas as pd
from collections import defaultdict
import base64

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="ShieldVault | Enterprise Threat Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- HELPER FUNCTION TO ENCODE LOCAL BG IMAGE -----------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Try loading and encoding logo1.png for the background
try:
    bin_str = get_base64_of_bin_file('logo1.png')
    bg_css = f"""
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(11, 15, 25, 0.88), rgba(11, 15, 25, 0.95)), 
                          url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #c0caf5;
    }}
    """
except Exception:
    # Fallback if logo1.png is missing or unreadable
    bg_css = """
    [data-testid="stAppViewContainer"] {
        background-color: #0b0f19;
        color: #c0caf5;
    }
    """

# ----------------- CUSTOM CSS FOR LOCAL BG IMAGE & EMBOSSED UI -----------------
st.markdown(f"""
    <style>
        {bg_css}
        
        /* Ensure content sits cleanly above the background */
        [data-testid="stAppViewContainer"] .main .block-container {{
            background-color: transparent;
        }}

        /* Sidebar Background (Deep Professional Blue) */
        [data-testid="stSidebar"] {{
            background-color: #0f172a;
            border-right: 1px solid #1e293b;
        }}
        
        /* Embossed Navigation Buttons in Blue Sidebar */
        div.stButton > button {{
            width: 100%;
            background: linear-gradient(145deg, #1e293b, #0f172a);
            color: #93c5fd;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
            font-size: 15px;
            box-shadow: 3px 3px 6px #070a12, -2px -2px 5px #172033;
            transition: all 0.2s ease-in-out;
            margin-bottom: 8px;
        }}

        /* Hover Effect for Embossed Buttons */
        div.stButton > button:hover {{
            color: #ffffff;
            border-color: #3b82f6;
            background: linear-gradient(145deg, #1d4ed8, #1e293b);
            box-shadow: inset 2px 2px 5px #070a12, inset -2px -2px 5px #172033;
        }}

        /* Active Focus Ring */
        div.stButton > button:focus {{
            color: #60a5fa !important;
            border: 1px solid #3b82f6 !important;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }}

        /* Metric Cards Styling - Glassmorphic look above the background */
        div[data-testid="stMetric"] {{
            background: rgba(17, 24, 39, 0.75);
            backdrop-filter: blur(10px);
            border: 1px solid #1e293b;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 4px 4px 10px #070a12;
        }}

        /* Hide Streamlit Branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR NAVIGATION & LOCAL LOGO -----------------
try:
    st.sidebar.image("logo.png", width=150)
except Exception:
    st.sidebar.markdown("<h3 style='color: #60a5fa; text-align: center;'>🛡️ SHIELD<b style='color: #ffffff;'>VAULT</b></h3>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='color: #64748b; font-size: 12px; text-align: center;'>AI Threat Intelligence v2.4</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Session State for Tab Routing
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Dashboard"

def set_tab(name):
    st.session_state.active_tab = name

# Custom Sidebar Embossed Navigation Buttons
st.sidebar.button("📊  Dashboard", on_click=set_tab, args=("Dashboard",))
st.sidebar.button("📈  Reports", on_click=set_tab, args=("Reports",))
st.sidebar.button("📄  Log Explorer", on_click=set_tab, args=("Logs",))
st.sidebar.button("🚨  Alert Feed", on_click=set_tab, args=("Alerts",))
st.sidebar.button("⚙️  System Settings", on_click=set_tab, args=("Settings",))

st.sidebar.markdown("---")
st.sidebar.markdown("<h4 style='color: #93c5fd;'>⚙️ Data Ingestion</h4>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload Server Logs (.txt)", type=["txt"])
threshold = st.sidebar.slider("Threat Sensitivity Threshold", min_value=2, max_value=10, value=3)

# ----------------- DATA LOGIC -----------------
lines = []
if uploaded_file is not None:
    lines = uploaded_file.getvalue().decode("utf-8").splitlines()

failed_attempts = defaultdict(int)
log_data = []

for line in lines:
    parts = line.split(" - - ")
    if len(parts) >= 2:
        ip = parts[0]
        rest = parts[1]
        status_code = rest.split(" ")[-2] if len(rest.split(" ")) >= 2 else "Unknown"
        log_data.append({"IP": ip, "Log Line": line, "Status": status_code})
        
        if "401" in line or status_code == "401":
            failed_attempts[ip] += 1

threats = {ip: count for ip, count in failed_attempts.items() if count >= threshold}

# ----------------- PAGE VIEWS -----------------

if st.session_state.active_tab == "Dashboard":
    st.markdown("<h2 style='color: #f8fafc; text-shadow: 2px 2px 4px #000000;'>SECURITY LOG ANALYSIS DASHBOARD</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-weight: 500;'>Real-Time Incident Response & Automated Pattern Recognition</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if uploaded_file is not None:
        c1, c2, c3 = st.columns(3)
        c1.metric("LOGS INGESTED", len(lines))
        c2.metric("CRITICAL THREATS", len(threats))
        c3.metric("UNIQUE ATTACK VECTORS", len(set(d['IP'] for d in log_data)))

        st.markdown("<br>", unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("<h4 style='color: #e2e8f0;'>📊 Attack Distribution by Source IP</h4>", unsafe_allow_html=True)
            if threats:
                chart_data = pd.DataFrame(list(threats.items()), columns=["IP", "Attempts"])
                st.bar_chart(chart_data.set_index("IP"))
            else:
                st.info("No malicious activity exceeding configured threshold.")

        with col_right:
            st.markdown("<h4 style='color: #e2e8f0;'>🚨 Flagged Incident Matrix</h4>", unsafe_allow_html=True)
            if threats:
                df = pd.DataFrame(list(threats.items()), columns=["Source IP", "Failed Attempts"])
                st.dataframe(df, use_container_width=True)
            else:
                st.success("All systems nominal.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #e2e8f0;'>🖥️ Real-time Telemetry Console</h4>", unsafe_allow_html=True)
        st.code("\n".join(lines[-6:]), language="bash")
    else:
        st.info("👈 Upload your `sample_logs.txt` file in the sidebar to activate the ShieldVault dashboard.")

elif st.session_state.active_tab == "Reports":
    st.markdown("<h2 style='color: #f8fafc;'>📈 Incident Audit & Compliance Reports</h2>", unsafe_allow_html=True)
    if lines:
        report_df = pd.DataFrame(log_data)
        st.dataframe(report_df, use_container_width=True)
        csv = report_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export SOC Summary (CSV)", csv, "shieldvault_report.csv", "text/csv")
    else:
        st.warning("No data ingested for report generation.")

elif st.session_state.active_tab == "Logs":
    st.markdown("<h2 style='color: #f8fafc;'>📄 Raw Log Stream Explorer</h2>", unsafe_allow_html=True)
    if lines:
        search = st.text_input("🔍 Filter logs by IP or Response Code:")
        filtered = [l for l in lines if search in l] if search else lines
        st.text_area("Console Output", "\n".join(filtered), height=450)
    else:
        st.info("Upload logs to inspect data.")

elif st.session_state.active_tab == "Alerts":
    st.markdown("<h2 style='color: #f8fafc;'>🚨 Live Threat Alert Feed</h2>", unsafe_allow_html=True)
    if threats:
        for ip, count in threats.items():
            st.error(f"🚨 **HIGH SEVERITY INCIDENT:** Multiple authentication failures detected from `{ip}` ({count} failed attempts). Recommended Action: Add to firewall drop rule.")
    else:
        st.success("No active critical alerts.")

elif st.session_state.active_tab == "Settings":
    st.markdown("<h2 style='color: #f8fafc;'>⚙️ Security Engine Configuration</h2>", unsafe_allow_html=True)
    st.text_input("Node Identifier", "us-east-sec-node-01")
    st.selectbox("Parsing Standard", ["Apache/Nginx Access Log", "AWS CloudTrail", "Syslog Key-Value"])
    st.slider("Automatic Firewall Rule Trigger", 1, 10, 5)
    st.button("Save System Parameters")