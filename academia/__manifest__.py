{
    'name': 'Academia de Idiomas - EduOdoo',
    'version': '19.0.1.0.0',
    'summary': 'Sistema Integral de Gestión para una Academia de Cursos',
    'description': """
        Módulo de gestión para academia de idiomas.
        - Gestión de cursos, sesiones, alumnos, clases, profesores
        - Facturación y matrículas
        - Campos computados y validaciones
        - Vistas avanzadas: calendario, kanban
    """,
    'author': 'EduOdoo',
    'category': 'Education',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/curso_views.xml',
        'views/sesion_views.xml',
        'views/alumno_views.xml',
        'views/clase_views.xml',
        'views/profesor_views.xml',
        'views/facturacion_views.xml',
        'views/matricula_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
