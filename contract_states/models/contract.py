# -*- coding: utf-8 -*-
from openerp import models, api, fields


class Contract(models.Model):
    _inherit = 'account.analytic.account'

    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'In Progress'),
        ('pending', 'To Renew'),
        ('close', 'Closed'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=False, copy=False, index=True, track_visibility='onchange', default='draft')
