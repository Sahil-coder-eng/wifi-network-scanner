# 🧠 Wi-Fi Network Scanner

A powerful tool that scans nearby Wi-Fi networks and displays signal strength, security type, and more.

---

## 🖥️ GUI Version (Tkinter)

- Dark mode desktop app using Python and Tkinter
- Visual signal strength with color-coded bars (🟩🟨🟥)
- Displays SSID, signal strength, and security protocol
- Export results to a CSV file
- Live scanning with refresh support
- Status bar for scan updates

---

## 🌐 Streamlit Version

- Web-based version built with Streamlit
- One-click scan, refresh, and CSV export
- Automatically adjusts based on platform (Local vs Cloud)
- Emoji-based signal indicators (🟩🟨🟥)
- Stylish UI with dark theme

### ⚙️ Live Mode vs Demo Mode

| Mode         | Local Machine | Streamlit Cloud |
|--------------|----------------|------------------|
| **Live Mode**  | ✅ Yes          | ❌ Not Supported |
| **Demo Mode**  | ✅ Yes          | ✅ Yes           |

### 🔍 How It Works:

- **Live Mode**: Uses the `pywifi` library to scan actual Wi-Fi networks using your system's wireless interface.
- **Demo Mode**: Displays mock Wi-Fi data (CU_WiFi, Public_WiFi) for showcasing the UI when scanning isn't possible.
- On **Streamlit Cloud**, only Demo Mode is allowed due to security restrictions (no hardware access).

The app auto-detects the environment and disables Live Mode in the cloud.

---

## 📂 Folder Structure

```
wifi-network-scanner/
├── gui_version/               # Tkinter GUI version
│   ├── wifi_scanner.py        # GUI app script
│   └── screenshot_gui.png     # Optional screenshot
│
├── streamlit_version/         # Streamlit app version
│   ├── streamlit_wifi_scanner.py
│   ├── requirements.txt       # Dependencies
│   └── screenshot_streamlit.png
│
├── README.md
└── .gitignore
```

---

## 🚀 Deployment Instructions

### 🔧 Local (Live Mode)
To run the Streamlit app locally with full Wi-Fi scanning support:

```bash
# Step into the project folder
cd streamlit_version

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_wifi_scanner.py
```

> ✅ This will launch the app in your browser and enable Live Mode scanning via pywifi.

### 🌐 Streamlit Cloud
1. Push project to GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Create a new app using the `streamlit_wifi_scanner.py` path
4. Only Demo Mode will be available online

---

## 📦 Requirements

Install required packages (for both versions):
```bash
pip install streamlit pywifi pandas
```
Or use:
```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Made with 💻 by Sahil Samal

---

✅ Feel free to fork, clone, and contribute!
link for demo https://wifi-network-scanner-4qnjlvvhhck5zfxausjnma.streamlit.app/
