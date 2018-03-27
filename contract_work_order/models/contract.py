# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.osv import orm
from odoo.tools.translate import _

WORK_PERIODICITY_TYPE = [
    ('none', 'None'),
    ('unique', 'Unique'),
    ('recursive', 'Recursive'),
    ('month', 'Specified Months'),]


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.one
    def plan_work_until_date(self):
        inc_month = self.company_id.work_planning_scope or 1
        date = fields.Datetime.now()[:10]
        time = datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        time = time+relativedelta(months=+inc_month)
        date = datetime.strftime(time, DEFAULT_SERVER_DATE_FORMAT)
        return date

    @api.one
    @api.depends('recurring_invoice_line_ids.recurring_next_work_date')
    def _compute_next_work_date(self):
        next_date = False
        for line in self.recurring_invoice_line_ids:
            if not next_date or (
                    line.recurring_next_work_date and
                    line.recurring_next_work_date < next_date):
                next_date = line.recurring_next_work_date
        self.computed_next_work_date = next_date

    @api.one
    @api.depends('recurring_invoice_line_ids.recurring_last_work_date')
    def _compute_last_work_date(self):
        last_date = False
        for line in self.recurring_invoice_line_ids:
            if not last_date or (
                    line.recurring_last_work_date and
                    line.recurring_last_work_date < last_date):
                last_date = line.recurring_last_work_date
        self.computed_last_work_date = last_date

    computed_next_work_date = fields.Date(
        string='Date of Next Work',
        compute='_compute_next_work_date')
    computed_last_work_date = fields.Date(
        string='Date of Next Work',
        compute='_compute_last_work_date')

    @api.one
    def _prepare_work(self):
        work = self._prepare_work_data()[0]
        lines = self._prepare_work_lines()[0]
        work['line_ids'] = (len(lines) > 0) and lines
        return work

    @api.one
    def _prepare_work_data(self):

        invoice = {
           'partner_id': self.partner_id.id,
           'project_id': self.id,
           'company_id': self.company_id.id or False,
           'date': self.computed_next_work_date
        }
        return invoice

    @api.one
    def _prepare_work_lines(self):
        work_lines = []
        work_date = self.computed_next_work_date
        #if work_date <= self.plan_work_until_date():
        for line in self.recurring_invoice_line_ids:
            if line.recurring_next_work_date == work_date:
                if line.periodicity_type not in (
                            'unique','recursive','month'):
                        continue
                line_value = line._prepare_work_line_data()[0]
                line.set_next_work_period_date()
                work_lines.append((0, 0, line_value))
        return work_lines

    def _recurring_create_work(self, automatic=False):

        work_ids = []
        #TODO Recuperar fecha de la compañia
        current_date = time.strftime('%Y-%m-%d')
        if self.id:
            contract_ids = self
        else:
            contract_ids = self.search(
                [('computed_next_work_date','<=', current_date),
                 ('active','=', True),
                 ('recurring_invoices','=', True)
                 ])
        for contract in contract_ids:
            work_values = contract._prepare_work()[0]
            if work_values['line_ids'] != []:
                work_ids.append(self.env['maintenance.work.order'].create( work_values))
        return work_ids

    def recurring_create_work(self):
        return self._recurring_create_work()

    def _cron_recurring_create_work(self):
        return self._recurring_create_work(automatic=True)

class AccountAnalyticInvoiceLine(models.Model):
    _inherit = "account.analytic.invoice.line"

    @api.onchange('product_id')
    def on_change_productid_update(self):
        self.price_unit = self.product_id.lst_price
        self.work_description = self.product_id.work_description
        self.name = self.product_id.name
        self.uom_id = self.product_id.uom_id

    @api.onchange('periodicity_type')
    def invoicebale_false(self):
        if self.periodicity_type != "none":
            self.work_to_invoice = False

    @api.onchange('periodicity_type')
    def on_change_work_periodici_type(self):
        if not self.recurring_last_work_date:
            self.recurring_next_work_date = self.analytic_account_id.date_start
        if self.work_periodicity_type == 'months':
            self.work_month_ids = False

    @api.onchange('month_ids')
    def on_change_work_month_ids(self):
        date = self.recurring_last_work_date or self.analytic_account_id.date_start
        time = datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        time = self.get_date_by_month(time, self.work_month_ids, next=False)
        date = datetime.strftime(time, DEFAULT_SERVER_DATE_FORMAT)
        self.recurring_next_work_date = date

    @api.one
    def set_next_work_period_date(self):
        date = self.recurring_next_work_date
        self.recurring_last_work_date = date
        time = datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        if self.work_periodicity_type == 'none':
            time = False
        elif self.work_periodicity_type == 'recursive':
            if self.work_recurring_rule_type == 'daily':
                time = time+relativedelta(days=+self.work_recurring_interval)
            elif self.work_recurring_rule_type == 'weekly':
                time = time+relativedelta(weeks=+self.work_recurring_interval)
            elif self.work_recurring_rule_type == 'monthly':
                time = time+relativedelta(months=+self.work_recurring_interval)
        elif self.work_periodicity_type == 'month' and len(self.work_month_ids) > 0:
            time = self.get_date_by_month(time, self.work_month_ids, next=True)
        next_date = time and datetime.strftime(
            time, DEFAULT_SERVER_DATE_FORMAT)
        self.recurring_next_work_date = next_date

    work_periodicity_type = fields.Selection(
        WORK_PERIODICITY_TYPE,
        default='none',
        string='Work Periodicity Type')
    work_recurring_rule_type = fields.Selection(
        [('daily', 'Day(s)'),
        ('weekly', 'Week(s)'),
        ('monthly', 'Month(s)'),
        ('yearly', 'Year(s)')],
        string='Work Recurrency',
        help="Work order automatically repeat at specified interval")
    work_recurring_interval = fields.Integer(
        string='Repeat Every',
        help="Repeat every (Days/Week/Month/Year)")
    work_month_ids = fields.Many2many(
        'contract.month',
        string='Months')
    recurring_next_work_date = fields.Date(
        string='Date To Work',
        default=fields.Date.context_today)
    recurring_last_work_date = fields.Date(
        string='Date Last Work',
        )
    work_description = fields.Html(
        string='Work Description')
    work_to_invoice = fields.Boolean(
        string='Invoiceable',
        default=False)

    @api.one
    def _prepare_work_line_data(self):
        values = {
            'product_id': self.product_id.id,
            'product_uom_qty': self.quantity,
            'product_uom_id': self.uom_id.id,
            'contract_line_id': self.id,
            'work_description': self.work_description,
            'to_invoice': self.work_to_invoice
        }
        return values
