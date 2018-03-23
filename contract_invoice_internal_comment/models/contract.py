# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    invoice_internal_comment = fields.Text(
        'Invoice Internal Information')

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        invoice = super(AccountAnalyticAccount, self)._prepare_invoice()
        invoice.update({
            'internal_comment': self.invoice_internal_comment})
        return invoice
