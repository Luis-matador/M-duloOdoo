from odoo import models, fields, api


class Clase(models.Model):
    _name = 'academia.clase'
    _description = 'Clase / Grupo de la Academia'

    nombre = fields.Char(string='Nombre', required=True)
    horario = fields.Char(string='Horario', required=True)
    dia_semana = fields.Selection([
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
    ], string='Día de la Semana', required=True)
    hora_inicio = fields.Float(string='Hora Inicio', required=True)
    hora_fin = fields.Float(string='Hora Fin', required=True)
    aula = fields.Char(string='Aula')
    capacidad_maxima = fields.Integer(string='Capacidad Máxima')

    # Many2one
    curso_id = fields.Many2one('academia.curso', string='Curso', required=True, ondelete='cascade')
    profesor_id = fields.Many2one('academia.profesor', string='Profesor', ondelete='set null')

    # Many2many: Alumnos de la clase
    alumno_ids = fields.Many2many(
        'academia.alumno',
        'academia_clase_alumno_rel',
        'clase_id',
        'alumno_id',
        string='Alumnos',
    )
