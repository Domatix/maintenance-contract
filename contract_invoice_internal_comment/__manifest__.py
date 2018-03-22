# -*- coding: utf-8 -*-
{
    'name': 'Contract Invoice Internal Comment',
    'version': '0.1',
    'author': 'Domatix',
    'summary': 'Contract Invoice Internal Comment',
    'website': 'http://www.domatix.com',
    'images': [],
    'depends': ['account_analytic_analysis'],
    'category': 'Sales Management',
    'data': [
        'views/contract_view.xml',
        'views/invoice_view.xml'
    ],
    'test': ['test/contract_partner.yml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
