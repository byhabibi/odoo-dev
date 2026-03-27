import xmlrpc.client
from datetime import datetime, timezone
import time

url = "http://localhost:8069"
db = "db_odoo"
username = "plc.gateway@gmail.com"
password = "7a02a8254c4e970a116b16beef47d874543fb0b1"

# Test Koneksi ke Odoo Server
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if not uid:
    print("❌ Auth failed")
    exit()

print("✅ Connected to Odoo UID:", uid)

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

counter = 0

while True:
    try:
        counter += 1

        models.execute_kw(
            db, uid, password,
            'plc.data', 'create',
            [{
                'counter': counter,
                'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            }]
        )

        print("✅ Data sent:", counter)

    except Exception as e:
        print("❌ Error:", e)

    time.sleep(2)