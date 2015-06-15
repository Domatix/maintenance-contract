# -*- coding: utf-8 -*-

from openerp.addons.contract_multiple_period.tests.common \
    import TestContractCommon
from openerp.tools import mute_logger


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
            'recurring_rule_type': 'monthly',
            'recurring_interval': 2
            }
        contract_lines.append((0, 0, line_values))
        contract_values = {
            'name': 'Maintenance of Servers RECURSIVE',
            'company_id': self.main_company,
            'partner_id': self.main_partner,
            'recurring_invoices': True,
            'recurring_invoice_line_ids': contract_lines
            }
        self.contract_recursive = self.ContractObj.create(contract_values)

        self.assertTrue(self.contract_recursive, "Contrato no creado")

        # FACTURO CONTRATO
        self.contract_recursive.recurring_create_invoice()

        invoice_ids = invoice_obj.search(
            [('invoice_line.account_analytic_id',
              '=',
              self.contract_recursive.id)])
        assert len(invoice_ids) >= 1, 'No invoice created for the contract'
