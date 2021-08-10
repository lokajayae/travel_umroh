# -*- coding: utf-8 -*-
# from odoo import http


# class TravelUmroh(http.Controller):
#     @http.route('/travel_umroh/travel_umroh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/travel_umroh/travel_umroh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('travel_umroh.listing', {
#             'root': '/travel_umroh/travel_umroh',
#             'objects': http.request.env['travel_umroh.travel_umroh'].search([]),
#         })

#     @http.route('/travel_umroh/travel_umroh/objects/<model("travel_umroh.travel_umroh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('travel_umroh.object', {
#             'object': obj
#         })
