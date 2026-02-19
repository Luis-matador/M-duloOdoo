from odoo import models, fields, api


class Matricula(models.Model):
    _name = 'academia.matricula'
    _description = 'Matrícula de Alumno'

    display_name = fields.Char(
        string='Nombre',
        compute='_compute_display_name',
        store=True,
    )
    fecha_matricula = fields.Date(string='Fecha de Matrícula', required=True, default=fields.Date.today)

    # Flujo de estados: borrador -> confirmada -> pagada
    state = fields.Selection([
        ('borrador', 'En Borrador'),
        ('confirmada', 'Confirmada'),
        ('pagada', 'Pagada'),
    ], string='Estado', required=True, default='borrador')

    # Many2one
    alumno_id = fields.Many2one('academia.alumno', string='Alumno', required=True, ondelete='cascade')
    sesion_id = fields.Many2one('academia.sesion', string='Sesión', required=True, ondelete='cascade')

    @api.depends('alumno_id.nombre_completo', 'sesion_id.display_name')
    def _compute_display_name(self):
        for rec in self:
            alumno = rec.alumno_id.nombre_completo or ''
            sesion = rec.sesion_id.display_name or ''
            rec.display_name = f"{alumno} - {sesion}" if alumno else sesion

    def action_confirmar(self):
        """Transición: borrador -> confirmada"""
        for rec in self:
            rec.state = 'confirmada'

    def action_pagar(self):
        """Transición: confirmada -> pagada"""
        for rec in self:
            rec.state = 'pagada'

    def action_borrador(self):
        """Volver a borrador"""
        for rec in self:
            rec.state = 'borrador'
