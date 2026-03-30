import xmlrpc.client
from datetime import datetime
import time

# PENGATURAN KONEKSI
url = "https://odoo.bybi.web.id" # Gunakan domain asli
db = "db_odoo"
username = "eng.monitoring@gmail.com"
api_key = "45603e0a18d52ea89f352241c9dd542af86adf15" 

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
            'mp': "Habibi", # Coba kirim nama MP agar navbar berubah
            'shift': "Shift 1"
        }

        try:
            res = models.execute_kw(db, uid, api_key, 'plc.data', 'create', [vals])
            print(f"✅ Data Sent [{res}]: Counter {counter}")
        except Exception as e:
            print(f"❌ Failed to send data: {e}")

        time.sleep(5) # Delay 5 detik biar nggak spamming server

except Exception as e:
    print(f"❌ Connection Error: {e}")