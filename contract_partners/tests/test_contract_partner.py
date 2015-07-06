# -*- coding: utf-8 -*-

from openerp.addons.contract_partners.tests.common \
    import TestContractCommon
from openerp.tools import mute_logger, float_round


class TestContractPartner(TestContractCommon):

    @mute_logger('openerp.addons.base.ir.ir_model', 'openerp.models')
    def test_00_contract_parner(self):
        """ Creo un contrato, le introduzco una direccion y compruebo que se ha creado bien """
        
        #crear un partner con direccion    
        self.parner_example = self.PartnerObj.create({'name':"Parner1",
                                                'street':"Street1",
                                               'city':"Valencia",
                                               'state_id':self.estateExample.id,
                                               'zip':"46026",
                                               'country_id': 5
                                               })   
        
        # CREAR CONTRATO CON LINEA MENSUAL
       
        contract_values = {
            'name': 'Maintenance of Servers',
            'company_id': self.main_company,
            'partner_id': self.main_partner,
            'recurring_invoices': False,
            'service_partner_id': self.parner_example.id ,
            'contact_partner_id': self.parner_example.id ,
            }
        
        self.contract = self.ContractObj.create(contract_values)
        self.assertTrue(self.contract, "Contrato no creado")
        
        #Compruebo que se ha generado correctamente la direccion de service_partner_id
        assert self.contract.service_partner_id.id != False, 'no se ha creado direccion en el campo service_partner_id!'
        
        #Compruebo que se ha generado correctamente la direccion de contact_partner_id
        assert self.contract.contact_partner_id.id != False, 'no se ha creado direccion en el campo contact_partner_id!'
        
        #Compruebo que la ciudad esta bien generada
        assert self.contract.service_partner_id.city == "Valencia", 'no se ha creado direccion en el campo contact_partner_id!'
    