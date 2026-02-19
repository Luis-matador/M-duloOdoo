from odoo import models, fields


class Facturacion(models.Model):
    _name = 'academia.facturacion'
    _description = 'Facturación de la Academia'

    numero_factura = fields.Char(string='Nº Factura', required=True)
    cantidad = fields.Float(string='Cantidad', required=True)
    fecha_pago = fields.Date(string='Fecha de Pago', required=True)
    concepto = fields.Char(string='Concepto', required=True)
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', required=True, default='pendiente')
    metodo_pago = fields.Char(string='Método de Pago')

    # Many2one
    alumno_id = fields.Many2one('academia.alumno', string='Alumno', required=True, ondelete='cascade')
    curso_id = fields.Many2one('academia.curso', string='Curso', ondelete='set null')
