# -*- coding: utf-8 -*-
import logging as logger#libreria para mandar errores
from odoo import models, fields, api
from odoo.exceptions import UserError #LIBRERIA PARA ERRORES DE ODOO (USUARIO)


class Presupuesto(models.Model):
    
    _name='presupuesto'#Tabla en BBDDs
    _inherit = ['image.mixin','mail.thread','mail.activity.mixin'] # Herencia para subir imagenes y descargarlas en diferentes calidades

    @api.depends('detalle_ids')
    def _compute_total(self):
        for record in self:
            subtotal=0
            for linea in record.detalle_ids:
                subtotal+=linea.importe
            record.base=subtotal
            record.impuestos=subtotal*0.16
            record.total= record.base+record.impuestos

    name=fields.Char(string='Pelicula')
    clasificacion= fields.Selection(selection=[
        ('G','G'), #Publico general
        ('PG','PG'),#Se recomienda la compañia de un adulto
        ('PG-13','PG-13'),#Mayores de 13
        ('R','R'),#EN compañia de un adulto obligatoriamente
        ('NC-17','NC-17'),#Mayores de 18
    ])
    fecha_estreno = fields.Date(string='Fecha estreno')
    puntuacion = fields.Integer(string='Puntuación', related='puntuacion2') #related : copiar , pegar : adquirir valor de otra variable
    puntuacion2 = fields.Integer(string='Puntuación2')
    active=fields.Boolean(string='Activo', default='true')
    #comdel_name : definir el modelo al cual se va a llamar
    
    
    director_id = fields.Many2one(comodel_name='res.partner', string='Director') #relacion uno a muchos debe llevar _id de prefrencia => /selector
    categoria_director_id = fields.Many2one(
        'res.partner.category',
        string='Categoria Director',
        #segunda version haciendo referencia a la data creada desde la carpeta "data"
        default=lambda self: self.env.ref('curso_udemy.category_director')
        #primera version
        #default=lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')])
        )
    genero_ids = fields.Many2many(comodel_name='genero', string='Genero') #relacion de muchos a muchos ids_ de prefrencia => /tabla
    vista_general = fields.Text(string='Descripción')
    link_trailer  = fields.Char(string='Trailer')
    es_libro = fields.Boolean(string='Version Libro')#Validacion
    libro  = fields.Binary(string='Libro')#Archivos (PDF , Excel)
    libro_filename  = fields.Char(string="Nombre del libro")
    state=fields.Selection(selection=[
        ('borrador','Borrador'),
        ('aprobado','Aprobado'),
        ('cancelado','Cancelado'),
    ], default='borrador', string='Estados', copy=False)
    fecha_aprobado=fields.Datetime(string="Fecha aprobado", copy=False)
    dsc_clasificacion=fields.Char(string="Desc")
    num_pre=fields.Char(string="Numero presupuesto", copy=False)
    fecha_creacion=fields.Datetime(string="Fecha creacion",copy=False, default=lambda self : fields.Datetime.now())

    actor_ids = fields.Many2many(comodel_name='res.partner', string='Actores') #relacion uno a muchos debe llevar _id de prefrencia => /selector
    categoria_actor_id = fields.Many2one(
        'res.partner.category',
        string='Categoria Actor',
        #segunda version haciendo referencia a la data creada desde la carpeta "data"
        default=lambda self: self.env.ref('curso_udemy.category_actor')
        )

    opinion=fields.Html(string="Opinion")
    
    detalle_ids=fields.One2many(
        comodel_name='presupuesto.detalle',
        inverse_name='presupuesto_id',
        string='Detalles'
    )

    currency_id=fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id,
    )
    terminos=fields.Text(string="Terminos")

    base=fields.Monetary(string='Base imponible', compute='_compute_total')

    impuestos=fields.Monetary(string='Impuestos', compute='_compute_total')

    total=fields.Monetary(string='Total', compute='_compute_total')

    def aprobar_presupuesto(self):
        self.state='aprobado'
        self.fecha_aprobado=fields.Datetime.now()

    def cancelar_presupuesto(self):
        self.state='cancelado'

    def unlink(self):
        logger.info('*********** Holiiiiiii')
        for record in self:
            if record.state =='cancelado':
                super(Presupuesto, record).unlink()#Sellama al nombre de la clase
            else:
                logger.info('*********** Nel perro')
                raise UserError('No se puede eliminar el registro')#Ya no se ejecuta nada debajo de este

    @api.model
    def create(self, variables):#se mandan los datos, ademas de usar decorador
        logger.info('******* var:{0}'.format(variables))
        seq_o=self.env['ir.sequence']
        correlativo=seq_o.next_by_code('secuencia.presupuesto.curso_udemy')
        variables['num_pre']=correlativo
        return super(Presupuesto, self).create(variables)

  
    def write(self, variables):    
        if 'clasificacion' in variables:
            raise UserError('La clasificacion no se puede editar')
        return super(Presupuesto, self).write(variables)


    @api.onchange('clasificacion')
    def _onchange_clasificacion(self):
        if self.clasificacion:
            if self.clasificacion=='G':
                self.dsc_clasificacion='Publico general'
            if self.clasificacion=='PG':
                self.dsc_clasificacion='Se recomienda la compañia de un adulto'
            if self.clasificacion=='PG-13':
                self.dsc_clasificacion='Mayores de 13'    
            if self.clasificacion=='R':
                self.dsc_clasificacion='En compañia de un adulto obligatoriamente'    
            if self.clasificacion=='NC-17':
                self.dsc_clasificacion='Mayores de 18' 
        else:
            self.dsc_clasificacion='False'

       
#lambda : EScribir una fincion directamente y no tener que hacer un llamdo / cuando la funcion es corta
#self.env[] : Saltar de un modelo a otro , depues de la funcion todo lo que se coloque va a partenever al modelo al cual se esta saltando y no afectara este

class PresupuestoDetalle(models.Model):
    _name="presupuesto.detalle"

    presupuesto_id=fields.Many2one(
        comodel_name='presupuesto',
        string='Presupuesto'
    )

    name=fields.Many2one(
        comodel_name='recurso.cinematografico',
        string='Recurso'
    )

    descripcion=fields.Char(string='Descripcion', related='name.descripcion')
    
    contacto_id=fields.Many2one(comodel_name='res.partner', string='Contacto',related='name.contacto_id')
 
    imagen=fields.Binary( 
        string='Imagen',
        related='name.imagen'
    )
    
    cantidad=fields.Float(string="Cantidad", default=1.0, digits=(16,4))
    precio=fields.Float(string="Precio", )
    importe=fields.Monetary(string="Importe")

    currency_id=fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        related="presupuesto_id.currency_id"
    )

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.precio=self.name.precio



    @api.onchange('cantidad','precio')
    def _onchange_importe(self):
        self.importe = self.cantidad * self.precio        
