# -*- coding: utf-8 -*-
{
    'name': 'Contract MRP Repair',
    'version': '11.0.0.1.0',
    'author': 'Domatix',
    'website': 'http://www.domatix.com',
    'images': [],
    'depends': ['contract', 'mrp_repair'],
    'category': 'Partner',
    'data': [
        'security/ir.model.access.csv',
        'views/contract_view.xml',
        'views/mrp_repair_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
