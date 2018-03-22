# -*- coding: utf-8 -*-

from odoo.addons.contract_discount.tests.common \
    import TestContractCommon
from odoo.tools import mute_logger, float_round


class TestContractRecursive(TestContractCommon):

    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.models')
    def test_00_contract_discount(self):
        """ Creo un producto con un descuento y compruebo que se aplica """
        
        # CREo lineas del contrato
        contract_lines = []
        
        line_values = {
            'quantity': 1.0,
            'price_unit': 75.0,
            'name': 'Database Administration',
            'product_id': self.product_consultant,
            'uom_id': self.uom_hour,
            'discount': 5,
            'contract_description_line':"Soy la descripcion html de un producto"
            }
        contract_lines.append((0,0,line_values))
       
      
        self.line = self.LineObj.create(line_values)

        assert self.line.price_subtotal == 71.25 , 'El valor calculado deberia ser 71.25'