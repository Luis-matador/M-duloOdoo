from odoo import models, fields, api


class Curso(models.Model):
    _name = 'academia.curso'
    _description = 'Curso de la Academia'

    titulo = fields.Char(string='Título', required=True)
    descripcion = fields.Text(string='Descripción')
    nivel = fields.Selection([
        ('a1', 'A1 - Principiante'),
        ('a2', 'A2 - Elemental'),
        ('b1', 'B1 - Intermedio'),
        ('b2', 'B2 - Intermedio Alto'),
        ('c1', 'C1 - Avanzado'),
        ('c2', 'C2 - Maestría'),
    ], string='Nivel', required=True)
    precio = fields.Float(string='Precio', required=True)

    # Many2one: Un curso tiene un profesor responsable
    profesor_id = fields.Many2one('academia.profesor', string='Profesor', ondelete='set null')

    # One2many: Un curso tiene muchas sesiones, clases, facturas
    sesion_ids = fields.One2many('academia.sesion', 'curso_id', string='Sesiones')
    clase_ids = fields.One2many('academia.clase', 'curso_id', string='Clases')
    facturacion_ids = fields.One2many('academia.facturacion', 'curso_id', string='Facturas')
