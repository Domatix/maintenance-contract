# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    service_partner_id = fields.Many2one(
        'res.partner',
        string="Service Address")

    contact_partner_id = fields.Many2one(
        'res.partner',
        string="Contact Address")

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        invoice = super(AccountAnalyticAccount, self)._prepare_invoice()
        invoice.update({
            'service_partner_id': self.service_partner_id
            and self.service_partner_id.id,
            'contact_partner_id': self.contact_partner_id
            and self.contact_partner_id.id})
        return invoice
