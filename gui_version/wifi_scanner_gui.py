import tkinter as tk
from tkinter import ttk, messagebox
import pywifi
from pywifi import const
import time
from datetime import datetime
import subprocess
import csv

# ---------- Helper Functions ----------

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

def signal_to_bars(signal):
    if signal >= -50:
        return "🟩🟩🟩🟩🟩"
    elif signal >= -60:
        return "🟩🟩🟩🟩"
    elif signal >= -70:
        return "🟨🟨🟨"
    elif signal >= -80:
        return "🟥🟥"
    else:
        return "⬛"

def get_connected_ssid():
    try:
        output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except:
        return "Unavailable"

def scan_networks(refreshing=False):
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        iface.scan()
        time.sleep(3)
        results = iface.scan_results()

        tree.delete(*tree.get_children())

        for i, network in enumerate(results):
            ssid = network.ssid or "<Hidden>"
            signal = network.signal
            bars = signal_to_bars(signal)
            signal_display = f"{signal} dBm {bars}"
            security = akm_type_to_string(network.akm[0]) if network.akm else "Open"
            if "Open" in security:
                security += " ⭐"
            tag = 'even' if i % 2 == 0 else 'odd'
            tree.insert("", tk.END, values=(ssid, signal_display, security), tags=(tag,))

        refresh_btn.config(state="normal")

        current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        timestamp_label.config(text=f"Last scanned: {current_time}")
        connected_label.config(text=f"📍 Connected to: {get_connected_ssid()}")
        status_bar.config(text=f"Found {len(results)} networks.")

        if refreshing:
            messagebox.showinfo("Scan Refreshed", "Wi-Fi networks refreshed!")
        else:
            messagebox.showinfo("Scan Complete", "Wi-Fi networks found!")

    except Exception as e:
        messagebox.showerror("Scan Failed", str(e))

def export_to_csv():
    if not tree.get_children():
        messagebox.showwarning("No Data", "No Wi-Fi networks to export.")
        return
    with open("wifi_networks.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["SSID", "Signal", "Security"])
        for row in tree.get_children():
            values = tree.item(row)["values"]
            writer.writerow(values)
    messagebox.showinfo("Export Complete", "Data exported to wifi_networks.csv")
    status_bar.config(text="Exported to wifi_networks.csv")

# ---------- GUI Setup ----------

root = tk.Tk()
root.title("📶 Wi-Fi Network Scanner")
root.geometry("720x540")
BG_COLOR = "#1e1e1e"
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#2e2e2e", fieldbackground="#2e2e2e",
                foreground="white", rowheight=25, font=("Segoe UI", 10, "bold"))
style.configure("Treeview.Heading", background="#333333", foreground="white", font=("Segoe UI", 11, "bold"))
style.map('Treeview', background=[('selected', '#444444')])

# Zebra row colors
tree_tags = {'odd': {'background': '#1f1f1f'}, 'even': {'background': '#2a2a2a'}}
for tag, cfg in tree_tags.items():
    style.configure(f"{tag}.Treeview", background=cfg['background'])

# Title and Labels
title = tk.Label(root, text="Wi-Fi Network Scanner", font=("Segoe UI", 16, "bold"), bg=BG_COLOR, fg="white")
title.pack(pady=10)

timestamp_label = tk.Label(root, text="Last scanned: Never", font=("Segoe UI", 10), bg=BG_COLOR, fg="#bbbbbb")
timestamp_label.pack()

connected_label = tk.Label(root, text="📍 Connected to: Detecting...", font=("Segoe UI", 10), fg="#33FF99", bg=BG_COLOR)
connected_label.pack(pady=5)

# Treeview
columns = ("SSID", "Signal", "Security")
tree = ttk.Treeview(root, columns=columns, show="headings", height=11)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=220)
tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=(10, 5))
tree.tag_configure('odd', background="#1f1f1f")
tree.tag_configure('even', background="#2a2a2a")

# Buttons
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=(5, 15))

scan_btn = ttk.Button(btn_frame, text="🔍 Scan Networks", command=lambda: scan_networks(refreshing=False))
scan_btn.grid(row=0, column=0, padx=10)

refresh_btn = ttk.Button(btn_frame, text="🔁 Refresh", command=lambda: scan_networks(refreshing=True), state="disabled")
refresh_btn.grid(row=0, column=1, padx=10)

export_btn = ttk.Button(btn_frame, text="📄 Export to CSV", command=export_to_csv)
export_btn.grid(row=0, column=2, padx=10)

exit_btn = ttk.Button(btn_frame, text="❌ Exit", command=root.quit)
exit_btn.grid(row=0, column=3, padx=10)

# Status Bar
status_bar = tk.Label(root, text="Ready", font=("Segoe UI", 9), anchor="w", bg=BG_COLOR, fg="#888888")
status_bar.pack(side="bottom", fill="x")

# Run GUI
root.mainloop()
# ---------- End of Code ----------
# This code creates a Wi-Fi scanner GUI using Tkinter and PyWiFi, allowing users to scan for Wi-Fi networks, view their details, refresh the list, and export the results to a CSV file. The GUI is styled with a modern dark theme and includes features like signal strength visualization and connected SSID detection.
# Ensure you have the required libraries installed: