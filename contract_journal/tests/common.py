# -*- coding: utf-8 -*-

from openerp.tests import common


class TestContractCommon(common.TransactionCase):

    def setUp(self):
        super(TestContractCommon, self).setUp()
        
        self.PartnerObj = self.env['res.partner']
        self.ModelDataObj = self.env['ir.model.data']
        self.ContractObj = self.env['account.analytic.account']
        self.InvoiceObj = self.env['account.invoice']
        self.PaymentObj = self.env['payment.mode']
        self.BankObj = self.env['res.partner.bank']
        self.JournalObj = self.env['account.journal']
        self.AccountObj = self.env['account.account']
        
        # Model Data
        self.main_company = self.ModelDataObj.xmlid_to_res_id(
            'base.main_company'
            )
        self.main_partner = self.ModelDataObj.xmlid_to_res_id(
            'base.main_partner'
            )
        self.uom_hour = self.ModelDataObj.xmlid_to_res_id(
            'product.product_uom_hour'
            )
        self.product_consultant = self.ModelDataObj.xmlid_to_res_id(
            'product.product_product_consultant'
            )
        
        self.bank_transfer = self.ModelDataObj.xmlid_to_res_id(
            'account_banking_payment_export.manual_bank_tranfer'
            )
        
        self.account_type = self.ModelDataObj.xmlid_to_res_id(
             'account.data_account_type_cash'
             )