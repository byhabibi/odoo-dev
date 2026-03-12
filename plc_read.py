from pymodbus.client import ModbusTcpClient
import requests
import time

PLC_IP = "192.168.1.10"
PLC_PORT = 502 #cek port plc 

ODOO_URL = "http://192.168.1.30:8069/api/plc_data"


def read_plc():

    client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

    if client.connect():

        result = client.read_holding_registers(address=0, count=4)

        if not result.isError():

            good = result.registers[0]
            reject = result.registers[1]
            status = result.registers[2]
            cycle = result.registers[3]

            payload = {
                "machine": "CNC01",
                "good": good,
                "reject": reject,
                "status": status,
                "cycle": cycle
            }

            try:
                response = requests.post(ODOO_URL, json=payload)
                print("Data sent to Odoo:", payload)

            except Exception as e:
                print("Failed to send data:", e)

        else:
            print("PLC read error")

        client.close()

    else:
        print("PLC connection failed")


while True:
    read_plc()
    time.sleep(1)