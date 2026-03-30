from odoo import models, fields

class PlcData(models.Model):
    _name = 'plc.data'
    _description = 'PLC Data'

    machine_name = fields.Char(string="Machine")
    counter = fields.Integer(string="Counter")
    timestamp = fields.Datetime(string="Time")