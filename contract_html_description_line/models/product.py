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


class ProductProduct(models.Model):
    _inherit = 'product.template'

    contract_description_line = fields.Html("Contract Description")


class ProductMeassure(models.Model):
    """ Operation Meassuer"""
    _name = 'product.meassure'

    name = fields.Char(
        string='Measure',
        required=True)
    notes = fields.Html(
        string='Notes')
    product_id = fields.Many2one(
        'product.template',
        string='Product')
    type = fields.Selection(
        [('check', 'Check'),('text', 'Text'),('number', 'Number')],
        string='Type')
