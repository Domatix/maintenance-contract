# -*- coding: utf-8 -*-

from openerp.addons.contract_work_order_measures.tests.common \
    import TestOrderMesasuresCommon
from openerp.tools import mute_logger, float_round
import time

class TestWorkOrder(TestOrderMesasuresCommon):

    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.models')
    def test_00_new_work_order(self):
        """ Creo una orden de trabajo desde un contrato con varias meassures lines """
        
        meassure_lines = []
        line_values ={
            'name': "Medida 1",
            'order_measure_type': 'number',
            'notes': "Estos son notas"
                      }
        meassure_lines.append((0,0,line_values))
        
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
            'meassure_ids':  meassure_lines
            }
        contract_lines.append((0,0,line_values))
        
          
        meassure_lines = []
        line_values ={
            'name': "Medida produc uno",
            'order_measure_type': 'number',
            'notes': "Estos son notas"
                      }
        meassure_lines.append((0,0,line_values))
        
        line_values ={
            'name': "Medida produc uno Dos",
            'order_measure_type': 'number',
            'notes': "Estos son notas"
                      }
        meassure_lines.append((0,0,line_values))
        
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
            'meassure_ids':  meassure_lines 
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
        self.contract.recurring_create_work_multiperiod()
        
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
        
        #print(work_id.line_ids)
        #assert len(work_id.line_ids[0])==1, 'Solo he introducido 1 meassure_id'
    