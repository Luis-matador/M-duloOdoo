from odoo import models, fields, api


class Profesor(models.Model):
    _name = 'academia.profesor'
    _description = 'Profesor de la Academia'

    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    email = fields.Char(string='Email')
    telefono = fields.Char(string='Teléfono')
    titulacion = fields.Char(string='Titulación', required=True)
    especialidad = fields.Char(string='Especialidad')
    nombre_completo = fields.Char(
        string='Nombre Completo',
        compute='_compute_nombre_completo',
        store=True,
    )
    fecha_contratacion = fields.Date(string='Fecha de Contratación')
    activo = fields.Boolean(string='Activo', default=True)

    # One2many inversos
    curso_ids = fields.One2many('academia.curso', 'profesor_id', string='Cursos que imparte')
    sesion_ids = fields.One2many('academia.sesion', 'profesor_id', string='Sesiones')
    clase_ids = fields.One2many('academia.clase', 'profesor_id', string='Clases')

    @api.depends('nombre', 'apellidos')
    def _compute_nombre_completo(self):
        for rec in self:
            rec.nombre_completo = f"{rec.nombre or ''} {rec.apellidos or ''}".strip()
