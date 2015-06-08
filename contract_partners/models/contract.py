# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    
    service_partner_id = fields.Many2one(
        'res.partner',
        string="Service Address"
        )
    
    contact_partner_id = fields.Many2one(
        'res.partner',
        string="Contact Address"
        )
    
    def _prepare_invoice_data(self, cr, uid, contract, context=None):
        context = context or {}
        invoice = super(AccountAnalyticAccount,self)._prepare_invoice_data(cr, uid, contract, context=context)
        invoice.update({
            'service_partner_id': contract.service_partner_id and contract.service_partner_id.id,
            'contact_partner_id': contract.contact_partner_id and contract.contact_partner_id.id,
            })
        return invoice
