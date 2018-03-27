# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = "account.analytic.invoice.line"

    @api.onchange('product_id')
    def on_change_productid_update_measure_type(self):
        measure_lines = []
        for line_product in self.product_id.measure_ids:
             measure_lines.append((0,0,{
                        'name':line_product.name,
                        'notes':line_product.notes,
                        'measure_id':line_product.measure_id.id}))
        self.update({'measure_ids':measure_lines})

    measure_ids = fields.One2many(
        'account.analytic.invoice.line.measure',
        'contract_line_id',
        string='Measures')

class AccountAnalyticInvoiceLineMeasure(models.Model):
    _name = "account.analytic.invoice.line.measure"

    name = fields.Char(
        string='Name',
        required=True)
    notes = fields.Html(
        string='Notes')
    contract_line_id = fields.Many2one(
        'account.analytic.invoice.line',
        string='Contract Line')
    measure_id = fields.Many2one(
        'contract.measure',
        string='Measure',
        required=True)

class AcountAnalyticAcountInvoice(models.Model):
    _inherit = "account.analytic.account"

    def recurring_create_work_multiperiod(self):
        work_order_id = self.recurring_create_work()[0]

        data_of_work_order = work_order_id
        #obtengo los datos de mi contrato
        data_of_contract = self

        measure_lines = []
        for invoice_line in data_of_contract.recurring_invoice_line_ids:
            for line_of_contract in invoice_line.measure_ids:
                measure_lines.append((0,0,{
                        'name':line_of_contract.name,
                        'notes':line_of_contract.notes,
                        'measure_id':line_of_contract.measure_id.id}))

        for line_of_work_order in data_of_work_order.line_ids:
            line_of_work_order.update({'measure_ids':measure_lines})
