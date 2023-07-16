# -*- coding: utf-8 -*-
{
    'name': "votaciones_uniacme",

    'summary': """
        Prueba Tecnica""",

    'description': """
        Prueba tecnica
    """,

    'author': "Juan Manuel Diaz",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        
        #Wizard 
        'wizards/import_proceso_votacion.xml',
        #Vistas
        'views/sedes_uniacme.xml',
        'views/personas.xml',
        'views/proceso_votaciones.xml',
        'views/votacion_online.xml',
        'report/resultados_votacion.xml',
        'views/website_menu.xml',
        'views/website_respuestas.xml',
        'views/website_proceso_votacion.xml',
        'views/website_seleccion_candidato.xml',
        
    
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
