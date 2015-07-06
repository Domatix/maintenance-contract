# -*- coding: utf-8 -*-
{
    'name': 'Contract html Description Line',
    'version': '0.1',
    'author': 'Domatix',
    'summary': 'Contract html Description Line',
    'website': 'http://www.domatix.com',
    'images': [],
    'depends': ['account_analytic_analysis',
                 'contract_html_description',
                 'contract_multiple_period'
                 ],
    'category': 'Sales Management',
    'data': [
        'views/contract_view.xml',
        'views/product_view.xml',
    ],
    'test': ['test/contract_journal.yml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
