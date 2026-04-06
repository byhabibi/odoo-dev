import xmlrpc.client
from datetime import datetime
import time

url = "https://odo.bybi.web.id" # 
db = "db_odoo"
username = "eng.monitoring@eranteknikatama.com"
api_key = "1b447b253e0d2e531adb55d9a57658788a771bbe" 

try:
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, api_key, {})
    
    if not uid:
        print("❌ Auth failed: Check Username/API Key")
        exit()
    print(f"✅ Connected! UID: {uid}")

    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    counter = 0

    while True:
        counter += 1
        # Data yang dikirim ke Odoo
        vals = {
            'counter': counter,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'man_power': 1, # Coba kirim nama MP agar navbar berubah
            'shift': "Shift 1"
        }

        try:
            res = models.execute_kw(db, uid, api_key, 'plc.data', 'create', [vals])
            print(f"✅ Data Sent [{res}]: Counter {counter}")
        except Exception as e:
            print(f"❌ Failed to send data: {e}")

        time.sleep(5)

except Exception as e:
    print(f"❌ Connection Error: {e}")