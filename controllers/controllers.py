# -*- coding: utf-8 -*-
# from odoo import http


# class CursoUdemy(http.Controller):
#     @http.route('/curso_udemy/curso_udemy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/curso_udemy/curso_udemy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('curso_udemy.listing', {
#             'root': '/curso_udemy/curso_udemy',
#             'objects': http.request.env['curso_udemy.curso_udemy'].search([]),
#         })

#     @http.route('/curso_udemy/curso_udemy/objects/<model("curso_udemy.curso_udemy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('curso_udemy.object', {
#             'object': obj
#         })
