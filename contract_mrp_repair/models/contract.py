from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.tools.translate import _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    recurring_repairs = fields.Boolean(
        string='Generate repair orders automatically',
    )
    repair_id = fields.One2many(
        comodel_name='mrp.repair',
        inverse_name='contract_id',
        string='Repairs')

    def _prepare_invoice_line(self, line, invoice_id):
        if self.recurring_repairs:
            repair_order = self.env['mrp.repair'].create({
                'contract_id': self.id,
                'partner_id': self.partner_id.id,
                'pricelist_id': self.pricelist_id and self.pricelist_id.id,
                'product_id': line.product_id.id,
                'product_qty': line.quantity,
                'product_uom': line.uom_id.id,
                'location_id': line._default_stock_location(),
                'location_dest_id': line._default_stock_location(),
                'internal_notes': line.internal_notes,
                'quotation_notes': line.quotation_notes

            })
            for operation in line.operations:
                repair_order.operations = [(0, 0, {
                    'name': operation.name,
                    'type': operation.type,
                    'product_id': operation.product_id.id,
                    'price_unit': operation.price_unit,
                    'product_uom_qty': operation.product_uom_qty,
                    'product_uom': operation.product_uom.id,
                    'location_id': operation.location_id.id,
                    'location_dest_id': operation.location_dest_id.id
                })]
            for fee in line.fees_lines:
                repair_order.fees_lines = [(0, 0, {
                    'name': fee.name,
                    'product_id': fee.product_id.id,
                    'price_unit': fee.price_unit,
                    'product_uom_qty': fee.product_uom_qty,
                    'product_uom': fee.product_uom.id,

                })]
        return super(AccountAnalyticAccount, self)._prepare_invoice_line(
            line, invoice_id)


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = "account.analytic.invoice.line"

    @api.model
    def default_get(self, fields):
        res = super(AccountAnalyticInvoiceLine, self).default_get(fields)
        res['recurring_repairs'] = self.env.context.get('recurring_repairs')
        return res

    @api.model
    def _default_stock_location(self):
        warehouse = self.env['stock.warehouse'].search([], limit=1)
        if warehouse:
            return warehouse.lot_stock_id.id
        return False

    recurring_repairs = fields.Boolean(
        string='Generate repair orders automatically',
        related="analytic_account_id.recurring_repairs"
    )

    operations = fields.One2many(
        'contract.mrp.repair.line', 'contract_line', 'Parts',
        copy=True)

    fees_lines = fields.One2many(
        'contract.mrp.repair.fee', 'contract_line', 'Operations',
        copy=True)
    guarantee_limit = fields.Date('Warranty Expiration')

    internal_notes = fields.Text('Internal Notes')
    quotation_notes = fields.Text('Quotation Notes')


class ContractRepairLine(models.Model):
    _name = 'contract.mrp.repair.line'
    _description = 'Contract Repair Line'

    name = fields.Char('Description', required=True)
    contract_line = fields.Many2one(
        'account.analytic.invoice.line', 'Contract Reference',
        index=True, ondelete='cascade')
    type = fields.Selection([
        ('add', 'Add'),
        ('remove', 'Remove')], 'Type', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Float('Subtotal', compute='_compute_price_subtotal', digits=0)
    tax_id = fields.Many2many(
        'account.tax', 'contract_repair_operation_line_tax', 'contract_repair_operation_line_id', 'tax_id', 'Taxes')
    product_uom_qty = fields.Float(
        'Quantity', default=1.0,
        digits=dp.get_precision('Product Unit of Measure'), required=True)
    product_uom = fields.Many2one(
        'product.uom', 'Product Unit of Measure',
        required=True)
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        index=True, required=True)
    location_dest_id = fields.Many2one(
        'stock.location', 'Dest. Location',
        index=True, required=True)

    @api.one
    @api.depends('price_unit', 'contract_line', 'product_uom_qty', 'product_id')
    def _compute_price_subtotal(self):
        taxes = self.tax_id.compute_all(self.price_unit, self.contract_line.analytic_account_id.pricelist_id.currency_id, self.product_uom_qty, self.product_id, self.contract_line.analytic_account_id.partner_id)
        self.price_subtotal = taxes['total_excluded']

    @api.onchange('contract_line', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        """ On change of product it sets product quantity, tax account, name,
        uom of product, unit price and price subtotal. """
        partner = self.contract_line.analytic_account_id.partner_id
        pricelist = self.contract_line.analytic_account_id.pricelist_id
        if not self.product_id or not self.product_uom_qty:
            return
        if self.product_id:
            if partner:
                self.name = self.product_id.with_context(lang=partner.lang).display_name
            else:
                self.name = self.product_id.display_name
            self.product_uom = self.product_id.uom_id.id
        if self.type != 'remove':
            if partner and self.product_id:
                self.tax_id = partner.property_account_position_id.map_tax(self.product_id.taxes_id, self.product_id, partner).ids
            warning = False
            if not pricelist:
                warning = {
                    'title': _('No Pricelist!'),
                    'message':
                        _('You have to select a pricelist in the Repair form !\n Please set one before choosing a product.')}
            else:
                price = pricelist.get_product_price(self.product_id, self.product_uom_qty, partner)
                if price is False:
                    warning = {
                        'title': _('No valid pricelist line found !'),
                        'message':
                            _("Couldn't find a pricelist line matching this product and quantity.\nYou have to change either the product, the quantity or the pricelist.")}
                else:
                    self.price_unit = price
            if warning:
                return {'warning': warning}

    @api.onchange('type', 'contract_line')
    def onchange_operation_type(self):
        """ On change of operation type it sets source location, destination location
        and to invoice field.
        @param product: Changed operation type.
        @param guarantee_limit: Guarantee limit of current record.
        @return: Dictionary of values.
        """
        if not self.type:
            self.location_id = False
            self.location_dest_id = False
        elif self.type == 'add':
            self.onchange_product_id()
            args = self.contract_line.analytic_account_id.company_id and [('company_id', '=', self.contract_line.analytic_account_id.company_id.id)] or []
            warehouse = self.env['stock.warehouse'].search(args, limit=1)
            self.location_id = warehouse.lot_stock_id
            self.location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
        else:
            self.price_unit = 0.0
            self.tax_id = False
            self.location_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
            self.location_dest_id = self.env['stock.location'].search([('scrap_location', '=', True)], limit=1).id


class ContractRepairFee(models.Model):
    _name = 'contract.mrp.repair.fee'
    _description = 'Contract Repair Fees Line'

    contract_line = fields.Many2one(
        'account.analytic.invoice.line', 'Contract Reference',
        index=True, ondelete='cascade', required=True)
    name = fields.Char('Description', index=True, required=True)
    product_id = fields.Many2one('product.product', 'Product')
    product_uom_qty = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    price_unit = fields.Float('Unit Price', required=True)
    product_uom = fields.Many2one('product.uom', 'Product Unit of Measure', required=True)
    price_subtotal = fields.Float('Subtotal', compute='_compute_price_subtotal', digits=0)
    tax_id = fields.Many2many('account.tax', 'contract_repair_fee_line_tax', 'contract_repair_fee_line_id', 'tax_id', 'Taxes')

    @api.one
    @api.depends('price_unit', 'contract_line', 'product_uom_qty', 'product_id')
    def _compute_price_subtotal(self):
        taxes = self.tax_id.compute_all(self.price_unit, self.contract_line.analytic_account_id.pricelist_id.currency_id, self.product_uom_qty, self.product_id, self.contract_line.analytic_account_id.partner_id)
        self.price_subtotal = taxes['total_excluded']

    @api.onchange('contract_line', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        """ On change of product it sets product quantity, tax account, name,
        uom of product, unit price and price subtotal. """
        if not self.product_id:
            return

        partner = self.contract_line.analytic_account_id.partner_id
        pricelist = self.contract_line.analytic_account_id.pricelist_id

        if partner and self.product_id:
            self.tax_id = partner.property_account_position_id.map_tax(self.product_id.taxes_id, self.product_id, partner).ids
        if self.product_id:
            self.name = self.product_id.display_name
            self.product_uom = self.product_id.uom_id.id

        warning = False
        if not pricelist:
            warning = {
                'title': _('No Pricelist!'),
                'message':
                    _('You have to select a pricelist in the Repair form !\n Please set one before choosing a product.')}
        else:
            price = pricelist.get_product_price(self.product_id, self.product_uom_qty, partner)
            if price is False:
                warning = {
                    'title': _('No valid pricelist line found !'),
                    'message':
                        _("Couldn't find a pricelist line matching this product and quantity.\nYou have to change either the product, the quantity or the pricelist.")}
            else:
                self.price_unit = price
        if warning:
            return {'warning': warning}
