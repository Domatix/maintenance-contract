# -*- coding: utf-8 -*-

from odoo.tests import common


class TestWorkCommon(common.TransactionCase):

    def setUp(self):
        super(TestWorkCommon, self).setUp()
        
        self.ProductObj = self.env['product.product']
        self.PartnerObj = self.env['res.partner']
        self.ModelDataObj = self.env['ir.model.data']
        self.ContractObj = self.env['account.analytic.account']
        self.workOrderObj = self.env['maintenance.work.order']
        
        
        # Model Data
        self.main_company = self.ModelDataObj.xmlid_to_res_id(
            'base.main_company'
            )
        self.main_partner = self.ModelDataObj.xmlid_to_res_id(
            'base.main_partner'
            )
        self.product_consultant = self.ModelDataObj.xmlid_to_res_id(
            'product.product_product_consultant'
            )
        self.uom_hour = self.ModelDataObj.xmlid_to_res_id(
            'product.product_uom_hour'
            )
        
        
        