# -*- coding: utf-8 -*-
{
    'name': 'Contract Discount multiple period',
    'version': '0.1',
    'category': 'Hidden',
    'author': 'Domatix',
    'summary': 'Contract Discount multiple period',
    'website': 'http://www.domatix.com',
    'images': [],
    'depends': ['contract_discount',
                'contract_multiple_period'],
    'category': 'Sales Management',
    'data': [
        'views/contract_view.xml',
    ],
    'test': ['test/contract_discount.yml'],
    'installable': True,
    'auto_install': True,
}
