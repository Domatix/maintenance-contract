# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

from datetime import datetime
import time

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

PERIODICITY_TYPE = [
    ('none', 'None'),
    ('unique', 'Unique'),
    ('recursive', 'Recursive'),
    ('month', 'Specified Months')]


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.one
    @api.depends('recurring_invoice_line_ids.recurring_next_date')
    def _compute_next_date(self):
        next_date = False
        for line in self.recurring_invoice_line_ids:
            if not next_date or (line.recurring_next_date and
                                 line.recurring_next_date < next_date):
                next_date = line.recurring_next_date
        if not next_date:
            next_date = self.date_start
        self.computed_next_date = next_date
        self.recurring_next_date = next_date

    # @api.depends('recurring_next_date', 'date_end', 'computed_next_date')
    # def _compute_create_invoice_visibility(self):
    #     for contract in self:
    #         contract.create_invoice_visibility = (
    #             not contract.date_end or
    #             contract.computed_next_date <= contract.date_end
    #         )

    @api.one
    @api.depends('recurring_invoice_line_ids.recurring_last_date')
    def _compute_last_date(self):
        last_date = False
        for line in self.recurring_invoice_line_ids:
            if not last_date or (
                    line.recurring_last_date and
                    line.recurring_last_date < last_date):
                last_date = line.recurring_last_date
        self.computed_last_date = last_date
        self.recurring_last_date = last_date

    periodicity_type = fields.Selection(
        PERIODICITY_TYPE,
        default='recursive',
        string='Periodicity Type'
        )
    month_ids = fields.Many2many(
        'contract.month',
        string='Months',
        readonly=False
        )
    computed_next_date = fields.Date(
        'Date of Next Invoice',
        compute='_compute_next_date',
        # store=True
        )
    computed_last_date = fields.Date(
        'Date of Last Invoice',
        compute='_compute_last_date',
        # store=True
        )

    @api.onchange('date_start')
    def onchange_date_start(self):
        self.computed_next_date = self.date_start

    @api.model
    def _prepare_invoice_line(self, line, invoice_id):
        date_for_invoice = line.analytic_account_id.computed_next_date
        if line.recurring_next_date:
            if line.recurring_next_date == date_for_invoice:
                if line.periodicity_type not in ('unique', 'recursive', 'month'):
                    return False
                vals = super(AccountAnalyticAccount, self)._prepare_invoice_line(
                    line, invoice_id)

                line.set_next_period_date()

                return vals
        else:
            return False

    @api.multi
    def _create_invoice(self):
        self.ensure_one()
        invoice_vals = self._prepare_invoice()
        invoice = self.env['account.invoice'].create(invoice_vals)
        for line in self.recurring_invoice_line_ids:
            invoice_line_vals = self._prepare_invoice_line(line, invoice.id)
            if invoice_line_vals:
                self.env['account.invoice.line'].create(invoice_line_vals)
        invoice.compute_taxes()
        return invoice

    # def _recurring_create_invoice(self, cr, uid, ids,
    #                               automatic=False, context=None):
    #     invoice_obj = self.pool['account.invoice']
    #     context = context or {}
    #     invoice_ids = []
    #     current_date = time.strftime('%Y-%m-%d')
    #     if ids:
    #         contract_ids = ids
    #     else:
    #         contract_ids = self.search(cr, uid,
    #                                    [('computed_next_date',
    #                                      '<=', current_date),
    #                                     ('state', '=', 'open'),
    #                                     ('recurring_invoices', '=', True),
    #                                     ('type', '=', 'contract')])
    #     if contract_ids:
    #         cr.execute(
    #             'SELECT company_id, array_agg(id) as ids '
    #             'FROM account_analytic_account '
    #             'WHERE id IN %s GROUP BY company_id', (tuple(contract_ids),))
    #         for c_id, ids in cr.fetchall():
    #             for contract in self.browse(cr, uid, ids,
    #                                         context=dict(context,
    #                                                      company_id=c_id,
    #                                                      force_company=c_id)):
    #                 try:
    #                     invoice_values = self._modify_recurring_date(cr, uid,
    #                                                            contract,
    #                                                            context=context)
    #                     if invoice_values['invoice_line'] != []:
    #                         invoice_ids.append(
    #                             invoice_obj.create(cr, uid,
    #                                                invoice_values,
    #                                                context=context))
    #                     if automatic:
    #                         cr.commit()
    #                 except Exception:
    #                     if automatic:
    #                         cr.rollback()
    #                     else:
    #                         raise
    #     return invoice_ids

    # def _modify_recurring_date(self):
    #     self.recurring_next_date = self.computed_next_date
    #     return self._prepare_invoice()


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = "account.analytic.invoice.line"

    @api.onchange('periodicity_type')
    def onchange_periodicity_type(self):
        if not self.recurring_last_date:
            self.recurring_next_date = \
                self.analytic_account_id.computed_next_date
        if self.periodicity_type == 'month':
            self.month_ids = False
        if self.periodicity_type == 'none':
            self.recurring_next_date = False

    @api.onchange('month_ids')
    def onchange_month_ids(self):
        date = self.recurring_last_date or self.analytic_account_id.date_start
        time = datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        time = self.get_date_by_month(time, self.month_ids, next=False)
        date = datetime.strftime(time, DEFAULT_SERVER_DATE_FORMAT)
        self.recurring_next_date = date

    @api.model
    def get_date_by_month(self, time, month_ids, next=False):
        if len(month_ids) > 0:
            allow_months = [int(m.code) for m in month_ids]
            allow_months.sort()
            time_month = time.month
            inc_month = 0
            if time_month > max(allow_months):
                inc_month = 12 - time_month + allow_months[0]
            else:
                if time_month > min(allow_months):
                    allow_months = [m for m in
                                    allow_months if m >= time_month]
                inc_month = allow_months[0] - time_month
            if next:
                month_actual = time_month + inc_month
                month_index = allow_months.index(month_actual)
                month_index = ((month_index < len(allow_months)-1)
                               and month_index + 1) or 0
                next_month = allow_months[month_index]
                inc_month = next_month - time_month
                if inc_month <= 0:
                    inc_month += 12
            time = time+relativedelta(months=+inc_month)
        return time

    @api.one
    def set_next_period_date(self):
        date = self.recurring_next_date
        self.recurring_last_date = date
        time = datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        if self.periodicity_type == 'none':
            time = False
        elif self.periodicity_type == 'recursive':
            if self.recurring_rule_type == 'daily':
                time = time+relativedelta(days=+self.recurring_interval)
            elif self.recurring_rule_type == 'weekly':
                time = time+relativedelta(weeks=+self.recurring_interval)
            elif self.recurring_rule_type == 'monthly':
                time = time+relativedelta(months=+self.recurring_interval)
        elif self.periodicity_type == 'month' and len(self.month_ids) > 0:
            time = self.get_date_by_month(time, self.month_ids, next=True)
        elif self.periodicity_type == 'unique':
            time = False
        next_date = time and datetime.strftime(
            time, DEFAULT_SERVER_DATE_FORMAT)
        self.recurring_next_date = next_date

    periodicity_type = fields.Selection(
        PERIODICITY_TYPE,
        string='Periodicity Type'
        )
    recurring_rule_type = fields.Selection(
        [
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)')],
        string='Recurrency',
        help="Invoice automatically repeat at specified interval"
        )
    recurring_interval = fields.Integer(
        string='Repeat Every',
        help="Repeat every (Days/Week/Month/Year)"
        )
    month_ids = fields.Many2many(
        'contract.month',
        string='Months',
        readonly=False)
    recurring_next_date = fields.Date(
        string='Date To Invoice',
        default=False)
    recurring_last_date = fields.Date(
        string='Date Last Invoice')
