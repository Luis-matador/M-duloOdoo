from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Sesion(models.Model):
    _name = 'academia.sesion'
    _description = 'Sesión de un Curso'

    display_name = fields.Char(
        string='Nombre',
        compute='_compute_display_name',
        store=True,
    )
    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En Curso'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', default='pendiente', required=True, group_expand='_expand_states')
    fecha_inicio = fields.Datetime(string='Fecha de Inicio', required=True)
    duracion = fields.Float(string='Duración (min)', required=True)
    num_asientos = fields.Integer(string='Número de Asientos', required=True)

    # Many2one
    curso_id = fields.Many2one('academia.curso', string='Curso', required=True, ondelete='cascade')
    profesor_id = fields.Many2one('academia.profesor', string='Profesor', ondelete='set null')

    # Many2many: Alumnos inscritos en la sesión
    alumno_ids = fields.Many2many(
        'academia.alumno',
        'academia_sesion_alumno_rel',
        'sesion_id',
        'alumno_id',
        string='Alumnos Inscritos',
    )

    # Campos computados
    asientos_disponibles = fields.Integer(
        string='Asientos Disponibles',
        compute='_compute_asientos',
        store=True,
    )
    porcentaje_ocupacion = fields.Float(
        string='% Ocupación',
        compute='_compute_asientos',
        store=True,
    )
    color = fields.Integer(
        string='Color',
        compute='_compute_asientos',
        store=True,
    )

    # One2many: matrículas de esta sesión
    matricula_ids = fields.One2many('academia.matricula', 'sesion_id', string='Matrículas')

    @api.model
    def _expand_states(self, states, domain):
        """Mostrar todas las columnas de estado en kanban aunque estén vacías."""
        return [key for key, _val in type(self).state.selection]

    @api.depends('curso_id.titulo', 'fecha_inicio')
    def _compute_display_name(self):
        for rec in self:
            titulo = rec.curso_id.titulo or ''
            fecha = rec.fecha_inicio.strftime('%d/%m/%Y %H:%M') if rec.fecha_inicio else ''
            rec.display_name = f"{titulo} - {fecha}" if titulo else fecha

    @api.depends('num_asientos', 'alumno_ids')
    def _compute_asientos(self):
        for rec in self:
            ocupados = len(rec.alumno_ids)
            rec.asientos_disponibles = rec.num_asientos - ocupados
            if rec.num_asientos > 0:
                rec.porcentaje_ocupacion = (ocupados / rec.num_asientos) * 100
            else:
                rec.porcentaje_ocupacion = 0.0
            # Color: 10 = verde (libre), 3 = amarillo (>50%), 1 = rojo (llena)
            if rec.porcentaje_ocupacion >= 100:
                rec.color = 1   # rojo
            elif rec.porcentaje_ocupacion >= 50:
                rec.color = 3   # amarillo
            else:
                rec.color = 10  # verde

    @api.constrains('alumno_ids', 'num_asientos')
    def _check_asientos(self):
        """No permitir que los alumnos inscritos superen el número de asientos."""
        for rec in self:
            if len(rec.alumno_ids) > rec.num_asientos:
                raise ValidationError(
                    f"La sesión '{rec.display_name}' tiene {len(rec.alumno_ids)} alumnos "
                    f"pero solo {rec.num_asientos} asientos disponibles."
                )

    @api.constrains('profesor_id', 'fecha_inicio', 'duracion')
    def _check_profesor_horario(self):
        """No permitir que un profesor dé dos sesiones a la misma hora."""
        for rec in self:
            if not rec.profesor_id or not rec.fecha_inicio:
                continue
            from datetime import timedelta
            fin = rec.fecha_inicio + timedelta(minutes=rec.duracion)
            conflicto = self.search([
                ('id', '!=', rec.id),
                ('profesor_id', '=', rec.profesor_id.id),
                ('fecha_inicio', '<', fin),
            ])
            # Filtrar las que realmente se solapan
            for otra in conflicto:
                otra_fin = otra.fecha_inicio + timedelta(minutes=otra.duracion)
                if otra.fecha_inicio < fin and otra_fin > rec.fecha_inicio:
                    raise ValidationError(
                        f"El profesor '{rec.profesor_id.nombre_completo}' ya tiene "
                        f"otra sesión programada en ese horario: '{otra.display_name}'."
                    )

    # ---- Transiciones de estado ----
    def action_confirmar(self):
        self.write({'state': 'confirmada'})

    def action_en_curso(self):
        self.write({'state': 'en_curso'})

    def action_finalizar(self):
        self.write({'state': 'finalizada'})

    def action_cancelar(self):
        self.write({'state': 'cancelada'})

    def action_pendiente(self):
        self.write({'state': 'pendiente'})
