from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
  _inherit = 'sale.order'

  travel_package_id = fields.Many2one(
    comodel_name = 'travel.package', 
    string='Travel Package',
    domain=[('state', '=', 'confirm')]
  )
    
  document_line = fields.One2many(
    comodel_name = 'sale.document.line', 
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
    if self.travel_package_id:
      order = self.env['sale.order'].new({
        'name' : self.name,
        'partner_id': self.partner_id.id,
        'partner_invoice_id' : self.partner_id.id,
        'partner_shipping_id' : self.partner_id.id,
        'pricelist_id': self.pricelist_id.id,
        'company_id' : self.company_id.id,
        'date_order': self.date_order
      })
      pp = self.travel_package_id
      new_order_line = self.env['sale.order.line'].new({
        'product_id': pp.product_id.id,
        'name' : '',
        'order_id': order.id,
        'product_uom_qty' : 1
      })
 
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
