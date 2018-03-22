# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    work_planning_scope = fields.Integer(
        string='Work Planning Scope',
        default=1,
        help='Number in month for planning work in contracts')