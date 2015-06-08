# -*- coding: utf-8 -*-
from openerp import models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    html_description = fields.Html(
        string='Description')
