# -*- coding: utf-8 -*-
from odoo import models, api


class Contract(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def set_draft(self):
        return self.write({'state': 'draft'})

    @api.multi
    def set_validate(self):
        return self.write({'state': 'open'})

    @api.model
    def default_get(self, fields):
        res = super(Contract, self).default_get(fields)
        res.update({'state': 'draft'})
        return res
