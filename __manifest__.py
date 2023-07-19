# -*- coding: utf-8 -*-
{
    'name': "modulo peliculas",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Peliculas',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['contacts', 'mail',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/update_wizard_view.xml',
        'report/reporte_pelicula.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/presupuesto.xml',
        'data/categoria.xml',
        'data/secuencia.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
