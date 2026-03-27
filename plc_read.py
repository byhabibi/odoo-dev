import xmlrpc.client
import sqlite3
import time
import logging
from datetime import datetime, timezone

# CONFIG
ODOO_URL = "http://localhost:8069"
DB = "db_odoo"
USERNAME = "by.habibi18@gmail.com"
PASSWORD = "bgatfbct"

MACHINE_NAME = "Bending 1"

POLL_INTERVAL = 2

# LOGGING
logging.basicConfig(
    filename="gateway.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# DATABASE BUFFER
conn = sqlite3.connect("gateway.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS buffer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    counter INTEGER,
    timestamp TEXT,
    sent INTEGER DEFAULT 0
)
""")

conn.commit()

# CONNECT ODOO
def connect_odoo():
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(DB, USERNAME, PASSWORD, {})

        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

        logging.info("Connected to Odoo")

        return uid, models

    except Exception as e:

        logging.error(f"Odoo connection failed: {e}")

        return None, None


uid, models = connect_odoo()

# SIMULASI PLC COUNTER
counter = 0
last_counter = None


def read_plc():

    global counter

    counter += 1

    return counter


def buffer_data(counter_value):

    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(
        "INSERT INTO buffer (counter, timestamp) VALUES (?, ?)",
        (counter_value, timestamp)
    )

    conn.commit()


def send_buffer():

    global uid, models

    rows = cursor.execute(
        """
        SELECT id, counter, timestamp
        FROM buffer
        WHERE sent = 0
        ORDER BY id ASC
        LIMIT 50
        """
    ).fetchall()

    if not rows:
        return

    for row in rows:

        id_, counter_val, ts = row

        try:

            models.execute_kw(
                DB, uid, PASSWORD,
                "plc.data", "create",
                [{
                    "machine_name": MACHINE_NAME,
                    "counter": counter_val,
                    "timestamp": ts
                }]
            )

            cursor.execute(
                "UPDATE buffer SET sent = 1 WHERE id = ?",
                (id_,)
            )

            conn.commit()

            logging.info(f"Sent data {counter_val}")

        except Exception as e:

            logging.error(f"Send failed: {e}")

            uid, models = connect_odoo()

            break


# WATCHDOG
last_heartbeat = time.time()

while True:

    try:

        plc_value = read_plc()

        if plc_value != last_counter:

            buffer_data(plc_value)

            logging.info(f"PLC read {plc_value}")

            last_counter = plc_value

        send_buffer()

        # heartbeat
        if time.time() - last_heartbeat > 60:

            logging.info("Gateway alive")

            last_heartbeat = time.time()

    except Exception as e:

        logging.error(f"Gateway error: {e}")

    time.sleep(POLL_INTERVAL)