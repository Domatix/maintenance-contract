from odoo import models, fields


class Repair(models.Model):
    _inherit = 'mrp.repair'

    contract_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Contract')
