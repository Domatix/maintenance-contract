# -*- coding: utf-8 -*-

from odoo.addons.contract_multiple_period.tests.common \
    import TestContractCommon
from odoo.tools import mute_logger


class TestContractRecursive(TestContractCommon):

    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.models')
    def test_00_contract_recursive_invoicing(self):
        """ Creo un contrato con una linea recursiva y lo facturo. """

        # CREAR CONTRATO CON LINEA RECURSIVA
        invoice_obj = self.env['account.invoice']
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
        contract_lines.append((0, 0, line_values))
        contract_values = {
            'name': 'Maintenance of Servers RECURSIVE',
            'company_id': self.main_company,
            'partner_id': self.main_partner,
            'recurring_invoices': True,
            'recurring_invoice_line_ids': contract_lines,
            }
        
        self.contract_recursive = self.ContractObj.create(contract_values)

        self.assertTrue(self.contract_recursive, "Contrato no creado")
        
        self.date_one =  self.contract_recursive.recurring_invoice_line_ids[0].recurring_next_date
        # FACTURO CONTRATO
        self.contract_recursive.recurring_create_invoice()
        
        invoice_ids = self.invoce_obj.search(
            [(
            'invoice_line.account_analytic_id',
            '=',
            self.contract_recursive.id
            )]
            )
        assert len(invoice_ids)>=1, 'No invoice created for the contract'
        
        self.date_two =  self.contract_recursive.recurring_invoice_line_ids[0].recurring_next_date
        
        #Sumo dos dias a la fecha inicial para ver si la fecha date_two se ha aumentado 2 dias como deberia ser
        self.date_one_more_two_days =date.today()+timedelta(days=2)
        
        assert(str(self.date_one_more_two_days) == str(self.date_two)),"This dates will be equal"
