# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    internal_comment = fields.Text(
        'Internal Information')
