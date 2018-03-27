# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
import openerp.addons.decimal_precision as dp
from odoo.exceptions import except_orm
from odoo.tools.translate import _
import time


class WorkOrder(models.Model):
    """ Maintenance Work Order """
    _name = 'maintenance.work.order'

    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        readonly=True,
        states={'draft': [('readonly', False)]},
        select=True,
        default='/')
    partner_id = fields.Many2one(
        'res.partner',
        'Customer',
        readonly=True,
        states={'draft': [('readonly', False)]},
        required=True,
        change_default=True,
        select=True,
        track_visibility='always')
    project_id = fields.Many2one(
        'account.analytic.account',
        string='Contract / Analytic', readonly=True,
        states={'draft': [('readonly', False)]},
        help="The analytic account related to a sales order.")
    company_id = fields.Many2one(
        'res.company',
        string='Company')
    sale_id = fields.Many2one(
        'sale.order',
        string='Sale Order')
    notes_todo = fields.Text(
        string='Work to do')
    notes_done = fields.Text(
        string='Work done')
    code = fields.Char(
        string='Code',
        required=False)
    date = fields.Date(
        string='Date',
        readonly=True)
    datetime_planned = fields.Datetime(
        string='Date Planned')
    datetime_done = fields.Datetime(
        string='Date Done')
    line_ids = fields.One2many(
        'maintenance.work.line',
        'work_order_id',
        string='Lines')
    state = fields.Selection(
        [('draft', 'Draft'),('planned', 'Planned'),
        ('done', 'Done'),('cancel', 'Cancelled')],
        string='Status',
        index=True,
        default='draft',
        track_visibility='onchange',
        copy=False)
    motive = fields.Char(
        string='Motive',
        readonly=True)

    @api.multi
    def work_planned(self):
        self.state = 'planned'

    @api.multi
    def work_done(self):
        self.state = 'done'
        self.datetime_done = fields.Datetime.now()
        for sale in self:
            sale.sale_id = sale.make_sale()[0]

    @api.multi
    def work_cancel(self):
        self.state = 'cancel'

    @api.one
    def make_sale(self):
        order_lines = []
        have_invoice_lines = False
        for line in self.line_ids:
            if line.to_invoice:
                have_invoice_lines = True
                order_lines.append((0, 0, {
                            'product_id': line.product_id.id,
                            'name': line.product_id.name,
                            'product_uom_qty': line.product_uom_qty,
                            'price_unit': line.product_id.list_price,
                       }))
        # I only entry to create sale.order if have line with the
        # field to_invoice: True
        if have_invoice_lines:
            warehouse_ids = self.env['stock.warehouse'].search([])
            if len(warehouse_ids) == 0:
                raise Warning(_('Its necessary have some warehouse.'))

            self.env['sale.order'].create({
                                    'partner_id': self.partner_id.id,
                                    'partner_invoice_id': self.partner_id.id,
                                    'partner_shipping_id': self.partner_id.id,
                                    'date_order': self.datetime_done,
                                    'warehouse_id':warehouse_ids[0].id,
                                    'pricelist_id': 1,
                                    'order_line': order_lines
                                    })


        # sale_id = False
        # partner_id = self.partner_id.id
        # date_order = self.datetime_done
        # vals = self.env['sale.order'].onchange_partner_id()
        # values = vals['value']
        # pricelist_id = values['pricelist_id']
        # if self.to_invoice:
        #     lines = []
        #     for line in self.line_ids:
        #         line_values = {}
        #         product_id = line.product_id.id
        #         product_uom_id = line.product_uom_id.id
        #         product_uom_qty = line.product_uom_qty
        #         vals = self.env['sale.order.line'].product_id_change(
        #                                               pricelist_id,
        #                                               product_id,
        #                                               product_uom_qty,
        #                                               product_uom_id,
        #                                               qty_uos=False,
        #                                               uos=False,
        #                                               name=False,
        #                                               partner_id=partner_id,
        #                                               lang=False,
        #                                               update_tax=True,
        #                                               date_order=date_order,
        #                                               packaging=False,
        #                                               flag=False)
        #         line_values = vals['value']
        #         line_values.update({
        #                        'product_id': product_id,
        #                        'product_uom_qty': product_uom_qty,
        #                        'product_uom_id': product_uom_id,
        #                })
        #         lines.append((0, 0, line_values))
        #     values.update({'partner_id': self.partner_id.id,
        #                    'date_order': self.datetime_done,
        #                    'project_id': self.project_id.id,
        #                    'partner_invoice_id': self.partner_invoice_id.id,
        #                    'partner_shipping_id': self.partner_shipping_id.id,
        #                    'order_line': lines,
        #                    'maintenance_sale': True
        #                    })
        #     sale_id = self.env['sale.order'].create(values)
        # #return False
        # return sale_id.id

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].get(
                                            'maintenance.work.order') or '/'
        if 'date' not in vals:
            vals['date'] = time.strftime('%Y-%m-%d')
        return super(WorkOrder, self).create(vals)

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        return self.env['sale.order'].onchange_partner_id(self.partner_id.id)


class WorkLine(models.Model):
    """ Maintenance Work Material """
    _name = 'maintenance.work.line'
    _rec_name = 'product_id'

    work_order_id = fields.Many2one(
        'maintenance.work.order',
        string='Work Order')
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True)
    product_uom_qty = fields.Float(
        string='Quantity',
        digits_compute=dp.get_precision('Product UoS'),
        required=True,
        default=1)
    product_uom_id = fields.Many2one(
        'product.uom',
        string='Unit of Measure ',
        required=True)
    sale_line_id = fields.Many2one(
        'sale.order.line',
        string='Sale Line')
    contract_line_id = fields.Many2one(
        'account.analytic.invoice.line',
        string='Contract Line')
    work_description = fields.Html(
        string='Work Description')
    to_invoice = fields.Boolean(
        string='Invoiceable',
        default=True,
        copy=False,
        readonly=False)

    @api.onchange('product_id', 'product_uom_id')
    def onchange_product_id(self):
        if not self.product_id:
            self.product_uom_id = False
        if self.product_uom_id:
            if self.product_id.uom_id.category_id.id != \
                                    self.product_uom_id.category_id.id:
                self.product_uom_id = False
        else:
            self.product_uom_id = self.product_id.uom_id.id
