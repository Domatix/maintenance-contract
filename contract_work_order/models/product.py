# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    work_description = fields.Html(
        string='Work Description')
