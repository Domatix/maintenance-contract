# -*- coding: utf-8 -*-

from odoo.tests import common


class TestContractCommon(common.TransactionCase):

    def setUp(self):
        super(TestContractCommon, self).setUp()
        
        self.PartnerObj = self.env['res.partner']
        self.ModelDataObj = self.env['ir.model.data']
        self.ContractObj = self.env['account.analytic.account']
        self.CountryObj = self.env['res.country']
        self.EstateObj = self.env['res.country.state']
        
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
        
        #self.countryExample = ES       
        self.estateExample = self.EstateObj.create({'name': "Valencia",
                                                    'code':"Val",
                                                   'country_id':5})