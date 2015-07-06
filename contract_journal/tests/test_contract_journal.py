# -*- coding: utf-8 -*-

from openerp.addons.contract_journal.tests.common \
    import TestContractCommon
from openerp.tools import mute_logger, float_round
import time

class TestContractPartner(TestContractCommon):

    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.models')
    def test_00_contract_journal(self):
        """ Creo un contrato, le introduzco un parner con metodo de pago """
        
        #Creo una forma de pago
        self.bank_example = self.BankObj.create({'state': 'bank','acc_number':26291919})
        
        self.account_example = self.AccountObj.create({
                                'code':661,
                                'name':"nombre",
                                'type':'liquidity',
                                'user_type': self.account_type,
                                'company_id':self.main_company 
                        })
       
        self.journal_example = self.JournalObj.create({
                               'name':"Efectivo",
                               'code': "dia",
                               'type': 'cash',
                               'default_debit_account_id':self.account_example.id,
                               'default_credit_account_id':self.account_example.id,
                               'company_id':self.main_company   
                        })
         
        
        
        # CREAR una linea de contrato
        contract_lines = []
        
        line_values = {
            'quantity': 2.0,
            'price_unit': 75.0,
            'name': 'Database Administration',
            'product_id': self.product_consultant,
            'uom_id': self.uom_hour,
            'periodicity_type': 'unique',
            'recurring_next_date':  time.strftime("%d/%m/%Y"),
            }
        contract_lines.append((0,0,line_values))
        
        
        # CREo un contrato con el metodo de pago anterior
        contract_values = {
            'name': 'Maintenance of Servers',
            'company_id': self.main_company,
            'partner_id': self.main_partner,
            'recurring_invoices': True,
            'recurring_invoice_line_ids': contract_lines, 
            'journal_id': self.journal_example.id
            }
        
        self.contract = self.ContractObj.create(contract_values)
        self.assertTrue(self.contract, "Contrato no creado")
        
        
        #Compruebo que el campo journal_id ha obtenido un valor valido
        assert self.contract.journal_id.id != False, 'no se ha creado correctamente el journal_id!'
        
  