# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.osv import orm
from odoo.tools.translate import _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    recurring_repairs = fields.Boolean(
        string='Generate repair orders',
    )

    def _prepare_invoice_line(self, line, invoice_id):
        # Create repair order
        self.env['mrp.repair'].create({
            'product_id': line.product_id,
        })
        return super(AccountAnalyticAccount, self)._prepare_invoice_line(
            line, invoice_id)


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = "account.analytic.invoice.line"

    operations = fields.One2many(
        'mrp.repair.line', 'repair_id', 'Parts',
        copy=True)

    fees_lines = fields.One2many(
        'mrp.repair.fee', 'repair_id', 'Operations',
        copy=True)
    guarantee_limit = fields.Date('Warranty Expiration')
    internal_notes = fields.Text('Internal Notes')
    quotation_notes = fields.Text('Quotation Notes')
