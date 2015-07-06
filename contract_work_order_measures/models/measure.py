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

from openerp import models, fields


class ContractMeasure(models.Model):
    """ Operation Meassuer"""
    _name = 'contract.measure'

    name = fields.Char(
        string='Measure',
        required=True)
    notes = fields.Html(
        string='Notes')
    type = fields.Selection(
        [('check', 'Check'),
        ('text', 'Text'),
        ('number', 'Number'),
        ('list', 'List of Values')],
        string='Type ')
    
    list_ids = fields.One2many(
        'contract.measure.list',
        'measure_id', string='List of values')


class ContractMeasureValuesList(models.Model):
    """ Operation Meassuer"""
    _name = 'contract.measure.list'
    
    measure_id = fields.Many2one(
        'contract.measure',
        string='Measure')
    name = fields.Char(
        string='name',
        required=True)
    