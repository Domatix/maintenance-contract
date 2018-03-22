# -*- coding: utf-8 -*-

from odoo.addons.contract_work_order.tests.common \
    import TestWorkCommon
from odoo.tools import mute_logger, float_round
import time

class TestWorkOrder(TestWorkCommon):

    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.models')
    def test_00_new_work_order(self):
        """ Creo una orden de trabajo desde un contrato """
        
        contract_lines = []
        
        line_values = {
            'quantity': 2.0,
            'price_unit': 75.0,
            'name': 'Database Administration',
            'product_id': self.product_consultant,
            'uom_id': self.uom_hour,
            'periodicity_type': 'recursive',
            'recurring_rule_type': 'daily',
            'recurring_interval': 2,
            'recurring_next_date':  time.strftime("%d/%m/%Y"), 
            }
        contract_lines.append((0,0,line_values))
        
        line_values = {
            'quantity': 1.0,
            'price_unit': 85.0,
            'name': 'Example 1',
            'product_id': self.product_consultant,
            'uom_id': self.uom_hour,
            'periodicity_type': 'recursive',
            'recurring_rule_type': 'daily',
            'recurring_interval': 2,
            'recurring_next_date':  time.strftime("%d/%m/%Y"), 
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
        
        # Creo la order de trabajo
        self.contract.recurring_create_work()
        
        work_id = self.workOrderObj.search(
            [(
            'project_id',
            '=',
            self.contract.id
            )]
            )
        assert len(work_id)==1, 'No se ha creado ningun orden de trabajo'
        
        #Compruebo que la orden de trabjo se ha creado con las dos lineas nesesarias.
        assert len(work_id.line_ids)==2, 'No se han creado las dos lineas que son nesesarias'
        
        
    