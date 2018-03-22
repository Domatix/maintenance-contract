# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.decimal_precision import decimal_precision as dp


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = "account.analytic.invoice.line"

    @api.one
    @api.depends('price_unit', 'discount')
    def _amount_line(self):
        currency_obj = self.env['res.currency']
        discount = self.discount / 100
        price_subtotal = self.quantity * self.price_unit * (1 - discount)
        if self.analytic_account_id.pricelist_id:
            cur = self.analytic_account_id.pricelist_id.currency_id
            price_subtotal = cur.round(price_subtotal)
        self.price_subtotal = price_subtotal

    discount = fields.Float(
        string='Discount (%)',
        digits=dp.get_precision('Discount'),
        default=0.0,
        required=True,
        help="e.g. 21, 16...")

    price_subtotal = fields.Float(
        string='Sub Total',
        digits=dp.get_precision('Account'),
        compute='_amount_line')

    def _prepare_invoice_lines(self, cr, uid, contract, fiscal_position_id, context=None):
        fpos_obj = self.pool.get('account.fiscal.position')
        fiscal_position = None
        if fiscal_position_id:
            fiscal_position = fpos_obj.browse(cr, uid,  fiscal_position_id, context=context)
        invoice_lines = []
        for line in contract.recurring_invoice_line_ids:

            res = line.product_id
            account_id = res.property_account_income.id
            if not account_id:
                account_id = res.categ_id.property_account_income_categ.id
            account_id = fpos_obj.map_account(cr, uid, fiscal_position, account_id)

            taxes = res.taxes_id or False
            tax_id = fpos_obj.map_tax(cr, uid, fiscal_position, taxes)
            price = line.price_unit or 0.0
            price = price * 1 ((line.discount or 0) / 100)
            invoice_lines.append((0, 0, {
                'name': line.name,
                'account_id': account_id,
                'account_analytic_id': contract.id,
                'price_unit': price,
                'quantity': line.quantity,
                'uos_id': line.uom_id.id or False,
                'product_id': line.product_id.id or False,
                'invoice_line_tax_id': [(6, 0, tax_id)],
            }))
        return invoice_lines