# -*- coding: utf-8 -*-
{
    'name': 'Contract Extension Work Orders',
    'version': '0.1',
    'author': 'Domatix',
    'summary': 'Contract Extension Work Orders',
    'website': 'http://www.domatix.com',
    'images': [],
    'depends': ['contract_multiple_period'],
    'category': 'Sales Management',
    'data': [
        'data/work_order_cron.xml',
        'data/work_order_sequence.xml',
        'data/work_order_workflow.xml',
        'views/contract_view.xml',
        'views/general_menu.xml',
        'views/work_order_view.xml',
        'views/product_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
