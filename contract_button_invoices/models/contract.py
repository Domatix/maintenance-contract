# -*- coding: utf-8 -*-
from odoo import models, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        invoice = super(AccountAnalyticAccount, self)._prepare_invoice()
        invoice.update({
            'analytic_account_id': self.id,
            })
        return invoice
