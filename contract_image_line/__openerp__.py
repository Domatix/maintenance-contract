# -*- coding: utf-8 -*-
{
    'name': 'Contract image product line',
    'version': '0.1',
    'author': 'Domatix',
    'summary': 'Contract html Description Line',
    'website': 'http://www.domatix.com',
    'images': [],
    'depends': ['account_analytic_analysis',
                 'contract_multiple_period',
                 'product_attachment_images',
                 ],
    'category': 'Sales Management',
    'data': [
        'views/contract_view.xml',
        #'views/product_view.xml',
    ],
    'test': ['test/contract_journal.yml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
