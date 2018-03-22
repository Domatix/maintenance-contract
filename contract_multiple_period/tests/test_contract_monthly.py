# -*- coding: utf-8 -*-
from odoo.addons.contract_multiple_period.tests.common \
    import TestContractCommon
from odoo.tools import mute_logger


class TestContractRecursive(TestContractCommon):

    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.models')
    def test_00_contract_monthly_invoicing(self):
        """ Creo un contrato con una linea recursiva y lo facturo. de tipo MES """

        # CREAR CONTRATO CON LINEA MENSUAL
        invoice_obj = self.env['account.invoice']
        contract_lines = []

        line_values = {
            'quantity': 2.0,
            'price_unit': 75.0,
            'name': 'Database Administration',
            'product_id': self.product_consultant,
            'uom_id': self.uom_hour,
            'periodicity_type': 'month',
            'month_ids': [(6, 0, self.months)]
            }
        contract_lines.append((0, 0, line_values))
        contract_values = {
            'name': 'Maintenance of Servers',
            'company_id': self.main_company,
            'partner_id': self.main_partner,
            'recurring_invoices': True,
            'recurring_invoice_line_ids': contract_lines
            }

        self.contract_monthly = self.ContractObj.create(contract_values)

        self.assertTrue(self.contract_monthly, "Contrato no creado")

        # FACTURO CONTRATO
        self.contract_monthly.recurring_create_invoice()
        
        invoice_ids = self.invoce_obj.search(
            [(
            'invoice_line.account_analytic_id',
            '=',
            self.contract_monthly.id
            )]
            )
        #TODO: Falta ver que fecha calcula con el mes indicado! este podria ser el fallo que siempre ocurre
        assert len(invoice_ids)>=1, 'No invoice created for the contract, FAIL becouse date not be calculated by the month'
