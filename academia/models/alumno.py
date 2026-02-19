from odoo import models, fields, api


class Alumno(models.Model):
    _name = 'academia.alumno'
    _description = 'Alumno de la Academia'

    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    email = fields.Char(string='Email', required=True)
    telefono = fields.Char(string='Teléfono')
    nombre_completo = fields.Char(
        string='Nombre Completo',
        compute='_compute_nombre_completo',
        store=True,
    )
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')

    # Many2many: Sesiones en las que está inscrito
    sesion_ids = fields.Many2many(
        'academia.sesion',
        'academia_sesion_alumno_rel',
        'alumno_id',
        'sesion_id',
        string='Sesiones',
    )

    # Many2many: Clases a las que asiste
    clase_ids = fields.Many2many(
        'academia.clase',
        'academia_clase_alumno_rel',
        'alumno_id',
        'clase_id',
        string='Clases',
    )

    # One2many
    matricula_ids = fields.One2many('academia.matricula', 'alumno_id', string='Matrículas')
    facturacion_ids = fields.One2many('academia.facturacion', 'alumno_id', string='Facturas')

    @api.depends('nombre', 'apellidos')
    def _compute_nombre_completo(self):
        for rec in self:
            rec.nombre_completo = f"{rec.nombre or ''} {rec.apellidos or ''}".strip()
