# -*- coding: utf-8 -*-

{
    'name': u'Exercice fiscal',
    'version': '1.0',
    'summary': u"Définition de l'exercice fiscal",
    'category': 'Accounting',
    'author': 'Andema',
    'website': 'http://www.andemaconsulting.com',
    'depends': [
        'account',
        'date_range'
    ],
    'data': [
        'data/date_range_type.xml',
        'views/date_range_type.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
