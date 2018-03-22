# -*- coding: utf-8 -*-

from odoo.addons.contract_multiple_period.tests.common \
    import TestContractCommon
from odoo.tools import mute_logger, float_round
import time


class TestContractRecursive(TestContractCommon):

    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.models')
    def test_00_contract_recursive_invoicing(self):
        """ Creo un contrato con una linea recursiva y lo facturo, Solo Deberia crear una factura tipo UNIQUE """
        # CREAR CONTRATO CON LINEA UNICA
        invoice_obj = self.env['account.invoice']
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
        contract_lines.append((0, 0, line_values))
        contract_values = {
            'name': 'Maintenance of Servers UNIQUE',
            'company_id': self.main_company,
            'partner_id': self.main_partner,
            'recurring_invoices': True,
            'recurring_invoice_line_ids': contract_lines
            }
        self.contract_unique = self.ContractObj.create(contract_values)

        self.assertTrue(self.contract_unique, "Contrato no creado")
        
        self.date_one =  self.contract_unique.recurring_invoice_line_ids[0].recurring_next_date
        # FACTURO CONTRATO
        self.contract_unique.recurring_create_invoice()
        
        invoice_ids = self.invoce_obj.search(
            [(
            'invoice_line.account_analytic_id',
            '=',
            self.contract_unique.id
            )]
            )
        
        assert len(invoice_ids)>=1, 'No invoice created for the contract'
        
        self.date_two =  self.contract_unique.recurring_invoice_line_ids[0].recurring_next_date
        
        #compruebo que la fecha ahora esta a false
        assert (self.date_two == False), 'This date will be False!'
        
         # FACTURO CONTRATO 2
        self.contract_unique.recurring_create_invoice()
        
        invoice_ids = self.invoce_obj.search(
            [(
            'invoice_line.account_analytic_id',
            '=',
            self.contract_unique.id
            )]
            )
        assert len(invoice_ids)<=2, 'second invoice is created but only one its will be created'
