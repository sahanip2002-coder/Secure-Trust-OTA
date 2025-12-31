import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
SERVER_URL = "https://127.0.0.1:8443"
session = requests.Session()
session.verify = False

def main():
    try:
        devices = session.get(f"{SERVER_URL}/api/devices").json()
    except:
        print("❌ Cannot connect to server."); return

    print(f"\n{'ID':<15} {'Status':<15} {'Version':<10}")
    print("-" * 45)
    d_list = list(devices.items())
    for i, (did, d) in enumerate(d_list):
        icon = "🟢" if d['status'] == "Stable" else "🔴"
        print(f"{i+1}. {did:<11} {icon} {d['status']:<12} v{d.get('version','?')}")
    
    sel = input("\nSelect device # to update: ")
    if not sel.isdigit(): return

    try: target = d_list[int(sel)-1][0]
    except: return

    print(f"\n🔄 Requesting OTA for {target}...")
    res = session.post(f"{SERVER_URL}/admin/deploy/{target}").json()
    
    if res.get('status') == 'blocked': print(f"🛡️  BLOCKED: {res.get('reason')}")
    elif res.get('status') == 'skipped': print(f"⏭️  SKIPPED: {res.get('reason')}")
    elif res.get('status') == 'initiated': print(f"✅ SUCCESS: Update to v{res.get('target_ver')} initiated")
    else: print(f"⚠️ Response: {res}")

if __name__ == "__main__":
    main()