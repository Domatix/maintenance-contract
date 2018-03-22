# -*- coding: utf-8 -*-
from odoo import models, fields


class ContractMonth(models.Model):
    _name = 'contract.month'

    code = fields.Integer(
        string='code'
        )
    name = fields.Char(
        string='Name'
        )
