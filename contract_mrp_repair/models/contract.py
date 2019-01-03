# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import time
from odoo.addons import decimal_precision as dp
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.osv import orm
from odoo.tools.translate import _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    recurring_repairs = fields.Boolean(
        string='Generate repair orders',
    )
    repair_id = fields.One2many(
        comodel_name='mrp.repair',
        inverse_name='contract_id',
        string='Repairs')


    def _prepare_invoice_line(self, line, invoice_id):
        # Create repair order
        self.env['mrp.repair'].create({
            'product_id': line.product_id,
        })
        return super(AccountAnalyticAccount, self)._prepare_invoice_line(
            line, invoice_id)


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = "account.analytic.invoice.line"

    # recurring_repairs = fields.Boolean(
    #     string='Generate repair orders',
    #     related="analytic_account_id.recurring_repairs"
    # )

    operations = fields.One2many(
        'contract.mrp.repair.line', 'contract_line', 'Parts',
        copy=True)

    fees_lines = fields.One2many(
        'contract.mrp.repair.fee', 'contract_line', 'Operations',
        copy=True)
    guarantee_limit = fields.Date('Warranty Expiration')
    internal_notes = fields.Text('Internal Notes')
    quotation_notes = fields.Text('Quotation Notes')


class ContractRepairLine(models.Model):
    _name = 'contract.mrp.repair.line'
    _description = 'Contract Repair Line'

    name = fields.Char('Description', required=True)
    contract_line = fields.Many2one(
        'account.analytic.invoice.line', 'Contract Reference',
        index=True, ondelete='cascade')
    type = fields.Selection([
        ('add', 'Add'),
        ('remove', 'Remove')], 'Type', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Float('Subtotal', compute='_compute_price_subtotal', digits=0)
    tax_id = fields.Many2many(
        'account.tax', 'contract_repair_operation_line_tax', 'contract_repair_operation_line_id', 'tax_id', 'Taxes')
    product_uom_qty = fields.Float(
        'Quantity', default=1.0,
        digits=dp.get_precision('Product Unit of Measure'), required=True)
    product_uom = fields.Many2one(
        'product.uom', 'Product Unit of Measure',
        required=True)

    @api.one
    @api.depends('price_unit', 'contract_line', 'product_uom_qty', 'product_id')
    def _compute_price_subtotal(self):
        taxes = self.tax_id.compute_all(self.price_unit, self.contract_line.analytic_account_id.pricelist_id.currency_id, self.product_uom_qty, self.product_id, self.contract_line.analytic_account_id.partner_id)
        self.price_subtotal = taxes['total_excluded']


class ContractRepairFee(models.Model):
    _name = 'contract.mrp.repair.fee'
    _description = 'Contract Repair Fees Line'

    contract_line = fields.Many2one(
        'account.analytic.invoice.line', 'Contract Reference',
        index=True, ondelete='cascade', required=True)
    name = fields.Char('Description', index=True, required=True)
    product_id = fields.Many2one('product.product', 'Product')
    product_uom_qty = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    price_unit = fields.Float('Unit Price', required=True)
    product_uom = fields.Many2one('product.uom', 'Product Unit of Measure', required=True)
    price_subtotal = fields.Float('Subtotal', compute='_compute_price_subtotal', digits=0)
    tax_id = fields.Many2many('account.tax', 'contract_repair_fee_line_tax', 'contract_repair_fee_line_id', 'tax_id', 'Taxes')

    @api.one
    @api.depends('price_unit', 'contract_line', 'product_uom_qty', 'product_id')
    def _compute_price_subtotal(self):
        taxes = self.tax_id.compute_all(self.price_unit, self.contract_line.analytic_account_id.pricelist_id.currency_id, self.product_uom_qty, self.product_id, self.contract_line.analytic_account_id.partner_id)
        self.price_subtotal = taxes['total_excluded']
