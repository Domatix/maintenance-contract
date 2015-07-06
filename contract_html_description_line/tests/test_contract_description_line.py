# -*- coding: utf-8 -*-

from openerp.addons.contract_html_description_line.tests.common \
    import TestContractCommon
from openerp.tools import mute_logger, float_round


class TestContractRecursive(TestContractCommon):

    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.models')
    def test_00_contract_monthly_invoicing(self):
        """ Creo un contrato con tres lineas, 2 con descripcion y 1 sin ella """
        
        # CREo lineas del contrato
        contract_lines = []
        
        line_values = {
            'quantity': 2.0,
            'price_unit': 75.0,
            'name': 'Database Administration',
            'product_id': self.product_consultant,
            'uom_id': self.uom_hour,
            'contract_description_line':"Soy la descripcion html de un producto"
            }
        contract_lines.append((0,0,line_values))
        
        line_values = {
            'quantity': 1.0,
            'price_unit': 35.0,
            'name': 'Database Administration',
            'product_id': self.product_consultant,
            'uom_id': self.uom_hour,
            }
        contract_lines.append((0,0,line_values))
        
        line_values = {
            'quantity': 1.0,
            'price_unit': 98.0,
            'name': 'Database Administration',
            'product_id': self.product_consultant,
            'uom_id': self.uom_hour,
            'contract_description_line':"Soy la descripcion html del ultimo producto"
            }
        contract_lines.append((0,0,line_values))
        
        contract_values = {
            'name': 'Maintenance of Servers',
            'company_id': self.main_company,
            'partner_id': self.main_partner,
            'recurring_invoices': True,
            'recurring_invoice_line_ids': contract_lines
            }

        self.contract = self.ContractObj.create(contract_values)
        self.assertTrue(self.contract, "Contrato no creado")
        
        #compruebo que la linea 1 y3 tienen descripcion y la 2 no
        assert self.contract.recurring_invoice_line_ids[0].contract_description_line != False , 'Esta linea no deberia estar vacia [0]'
        assert self.contract.recurring_invoice_line_ids[1].contract_description_line == False , 'Esta linea deberia estar vacia [1]'  
        assert self.contract.recurring_invoice_line_ids[2].contract_description_line != False , 'Esta linea no deberia estar vacia [2]'     
        
        
       