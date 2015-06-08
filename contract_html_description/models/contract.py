# -*- coding: utf-8 -*-
from openerp import models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    description_html = fields.Html(
        string='Description')
