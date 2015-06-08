# -*- coding: utf-8 -*-
from openerp import models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    invoice_internal_comment = fields.Text(
        'Invoice Internal Information')

    def _prepare_invoice_data(self, cr, uid, contract, context=None):
        context = context or {}
        invoice = super(AccountAnalyticAccount, self)._prepare_invoice_data(
            cr, uid, contract, context=context)
        invoice.update({
            'internal_comment': contract.invoice_internal_comment})
        return invoice
