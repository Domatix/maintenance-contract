# -*- coding: utf-8 -*-
from openerp import models, fields, api

class AccountAnalyticAccountInherit(models.Model):
    _inherit = 'account.analytic.invoice.line'

    @api.onchange('product_id')
    def on_change_productid_update_contract_description(self):
        self.contract_description_line = self.product_id.contract_description_line
    
    contract_description_line = fields.Html("Contract Description")
    