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

from openerp import models, fields, api
from openerp.tools.translate import _

class WorkLine(models.Model):
    """ Maintenance Work Line """
    _inherit = 'maintenance.work.line'
    
    measure_ids = fields.One2many(
        'maintenance.work.line.measure',
        'work_order_line_id',
        string='Measures')

class WorkLineMeassure(models.Model):
    """ Maintenance Work Line Meassure"""
    _name = 'maintenance.work.line.measure'
    
    @api.onchange('measure_id')
    def onchange_measure_id(self):
        self.type = self.measure_id and self.measure_id.type
        
    @api.one
    @api.depends('type', 'value_check', 'value_char',
            'value_number', 'value_list')
    def _get_computed_value(self):
        if self.type == 'check':
            self.computed_value = self.value_check
        elif self.type == 'text':
            self.computed_value = self.value_text
        elif self.type == 'number':
            self.computed_value = self.value_number
        elif self.type == 'list':
            self.computed_value = self.value_list.name
        else:
            self.computed_value = False

    work_order_line_id = fields.Many2one(
        'maintenance.work.line',
        string='Work Order Line')
    name = fields.Char(
        string='Meassure')
    notes = fields.Html(
        string='Notes')
    measure_id = fields.Many2one(
        'contract.measure',
        string='Measure')
    type = fields.Selection(
        [('check', 'Check'),
        ('text', 'Text'),
        ('number', 'Number'),
        ('list', 'List of Values')],
        string='Type ')
    value_check = fields.Boolean(
        string='Value')
    value_char = fields.Char(
        string='Value')
    value_number = fields.Float(
        string='Value')
    value_list = fields.Many2one(
        'contract.measure.list',
        string="Value")
    computed_value = fields.Char(
        string="Value",
        compute="_get_computed_value")
