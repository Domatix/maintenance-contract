# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    def _default_journal(self):
        company_id = self._context.get(
            'company_id', self.env.user.company_id.id)
        domain = [
            ('type', '=', 'sale'),
            ('company_id', '=', company_id)]
        return self.env['account.journal'].search(domain, limit=1)

    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        default=_default_journal,
        domain="[('type', '=', 'sale'),('company_id', '=', company_id)]")

    def _prepare_invoice_data(self, cr, uid, contract, context=None):
        context = context or {}
        invoice = super(AccountAnalyticAccount, self)._prepare_invoice_data(
            cr, uid, contract, context=context)
        invoice.update({
            'journal_id': contract.journal_id
            and contract.journal_id.id or invoice['journal_id']})
        return invoice
