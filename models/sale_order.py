from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    travel_package_id = fields.Many2one(
      comodel = 'travel.package', 
      string='Travel Package',
      domain=[('state', '=', 'confirm')]
    )

    hotel_line_ids = fields.One2many(
        comodel_name='hotel.line',
        inverse_name='package_id',
        string='Related Hotels',
    )
    
    document_line = fields.One2many(
      comodel_name = 'sale.dokumen.line', 
      inverse_name = 'order_id', 
      string='Document Lines'
    )
    passport_line = fields.One2many(
      comodel_name = 'sale.passport.line', 
      inverse_name = 'order_id', 
      string='Passport Lines'
    )

    @api.onchange('travel_package_id')
    def set_order_line(self):
      res = {}
      if self.paket_perjalanan_id:
        pp = self.paket_perjalanan_id
 
        ### Otomatis - Nilai di set otomatis dari method onchange product_id_change() ###
        order = self.env['sale.order'].new({
          'partner_id': self.partner_id.id,
          'pricelist_id': self.pricelist_id.id,
          'date_order': self.date_order
        })
        
        line = self.env['sale.order.line'].new({'product_id': pp.product_id.id, 'order_id': order.id})
        line.product_id_change()
        vals = line._convert_to_write({name: line[name] for name in line._cache})
        res['value'] = {'order_line': [vals]}
 
        ### Manual - Nilai di set secara manual ###
        
        # res['value'] = {
        #     'order_line': [{
        #         'product_id': pp.product_id.id,
        #         'name':  pp.product_id.partner_ref,
        #         'product_uom_qty': 1,
        #         'product_uom': pp.product_id.uom_id.id,
        #         'price_unit': pp.product_id.lst_price
        #     }]
        # }
        return res
 
class SaleDocumentLine(models.Model):
  _name = "sale.document.line"
  
  order_id = fields.Many2one(
    comodel_name = 'sale.order', 
    string='Sales Orders', 
    ondelete='cascade'
  )
  name = fields.Char(
    string='Name', 
    required=True
  )
  photo = fields.Binary(
    string='Photo', 
    required=True
  )
 
class SalePassportLine(models.Model):
  _name = "sale.passport.line"
  
  order_id = fields.Many2one(
    comodel_name = 'sale.order', 
    string='Sales Orders', 
    ondelete='cascade'
  )
  partner_id = fields.Many2one(
    comodel_name = 'res.partner', 
    string='Jamaah', 
    required=True
  )
  passport_number = fields.Char(
    string='Passport Number', 
    required=True
  )
  name = fields.Char(
    string='Name in Passport', 
    required=True
  )
  expiry = fields.Date(
    string='Date of Expiry', 
    required=True
  )
  room_type = fields.Selection(
    [('d', 'Double'), 
     ('t', 'Triple'), 
     ('q', 'Quad')], 
    string='Room Type', 
    required=True
  )
  photo = fields.Binary(
    string='Photo', 
    required=True
  )

    