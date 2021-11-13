# -*- coding: utf-8 -*-
# from odoo import http


# class Task(http.Controller):
#     @http.route('/task/task/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/task/task/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('task.listing', {
#             'root': '/task/task',
#             'objects': http.request.env['task.task'].search([]),
#         })

#     @http.route('/task/task/objects/<model("task.task"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('task.object', {
#             'object': obj
#         })
