# -*- coding: utf-8 -*-
{
    'name': 'Contract Multiple Period',
    'version': '0.1',
    'author': 'Domatix',
    'summary': 'Contract Multiple Period',
    'website': 'http://www.domatix.com',
    'images': [],
    'depends': ['contract'],
    'category': 'Sales Management',
    'data': [
        'views/contract_view.xml',
        'data/month_data.xml',
        'security/ir.model.access.csv'
    ],
    #'test': ['test/contract_multiple_period.yml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
