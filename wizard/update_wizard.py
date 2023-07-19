# -*- coding: utf-8 -*-


from odoo import models, fields, api


class UpdateWizard(models.TransientModel):#->Datas temporales,usar para popups
    _name="update.wizard"
    name=fields.Text(string='Nueva desc')

    def update_vista_general(self):
        presupuesto_object=self.env['presupuesto']
        #presupuesto_id=presupuesto_object.search([('id','=',self._context['active_id'])])#->hacer la busqueda con campo especifico
        presupuesto_id=presupuesto_object.browse(self._context['active_id'])#->BUsqueda por ID, odoo asume que hay un id para validar
        presupuesto_id.vista_general=self.name



