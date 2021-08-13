from odoo import models, fields, api

class TravelPackage(models.Model):
    _name = "travel.package"

    name = fields.Char(
      string="Reference",
      readonly=True,
      default="/"
    )
    product_id = fields.Many2one(
      comodel_name="product.product",
      string="Package",
      required=True,
      readonly=True, 
      states={'draft': [('readonly', False)]}
    )
    departure_date = fields.Date(
      string="Departure Date",
      required=True,
      readonly=True, 
      states={'draft': [('readonly', False)]}
    )
    arrival_date = fields.Date(
      string="Arrival Date",
      required=True, 
      readonly=True, 
      states={'draft': [('readonly', False)]}
    )
    quota = fields.Integer(
      string="Quota",
      readonly=True, 
      states={'draft': [('readonly', False)]}
    )
    quota_progress = fields.Float(
      string="Quota Progress",
      compute ="_taken_seats"
    )
    note = fields.Text(
      string="Notes",
      readonly=True, 
      states={'draft': [('readonly', False)]}
    )
    hotel_line = fields.One2many(
        comodel_name='hotel.line.package',
        inverse_name='travel_package_id',
        string='Hotel Line',
        readonly=True, 
        states={'draft': [('readonly', False)]}
    )
    airline_line = fields.One2many(
        comodel_name='airline.line.package',
        inverse_name='travel_package_id',
        string='Airline Line',
        readonly=True, 
        states={'draft': [('readonly', False)]}
    )
    schedule_line = fields.One2many(
        comodel_name='schedule.line.package',
        inverse_name='travel_package_id',
        string='Schedule Line',
        readonly=True, 
        states={'draft': [('readonly', False)]}
    )
    participant_line = fields.One2many(
      comodel_name = 'participant.line.package', 
      inverse_name='travel_package_id', 
      string='Jamaah Line', 
      readonly=True, 
    )
    state = fields.Selection([
      ('draft', 'Draft'),
      ('confirm', 'Confirmed')], 
      string='Status', 
      readonly=True, 
      copy=False, 
      default='draft', 
      track_visibility='onchange'
    )

    def action_confirm(self):
      self.write({'state': 'confirm'})

    @api.model
    def create(self, vals) :
      vals['name'] = self.env['ir.sequence'].next_by_code('travel.package')
      return super(TravelPackage, self).create(vals)
    
    def name_get(self):
      return [(this.id, this.name + "#" + " " + this.product_id.partner_ref) for this in self]

    @api.depends('quota', 'participant_line')
    def _taken_seats(self):
      for r in self:
        if not r.quota:
          r.quota_progress = 0.0
        else:
          r.quota_progress = 100.0 * len(r.participant_line) / r.quota

    def update_participant(self) :
      order_ids = self.env['sale.order'].search([('travel_package_id', '=', self.id), ('state', 'not in', ('draft', 'cancel'))])
      print(order_ids)
      if order_ids:
        self.participant_line.unlink()
        for order in order_ids:
          for passport in order.passport_line:
            print(passport.name)
            self.participant_line.create({
              'travel_package_id': self.id,
              'partner_id': passport.partner_id.id,
              'name': passport.name,
              'order_id': order.id,
              'gender': passport.partner_id.gender,
              'room_type': passport.room_type,
            })

class AirlineLinePackage(models.Model):
  _name = "airline.line.package"
    
  travel_package_id = fields.Many2one(
    'travel.package', 
    string='Travel Package', 
    ondelete='cascade'
  )
  partner_id = fields.Many2one(
    'res.partner', 
    string='Airlines', 
    required=True
  )
  departure_date = fields.Date(
    string='Departure Date', 
    required=True
  )
  departure_city = fields.Char(
    string='Departure City', 
    required=True
  )
  arrival_city = fields.Char(
    'Arrival City', 
    required=True
  )

class ParticipantLinePackage(models.Model):
    _name = "participant.line.package"
    
    travel_package_id = fields.Many2one(
      'travel.package', 
      string='Travel Package', 
      ondelete='cascade'
    )
    partner_id = fields.Many2one(
      'res.partner', 
      string='Jamaah'
    )
    name = fields.Char(
      string='Name in Passport'
    )
    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sales Order',
    )
    gender = fields.Selection(
      [('male', 'Male'),
       ('female', 'Female')],
      string='Gender'
    )
    room_type = fields.Selection(
      [('d', 'Double'), 
       ('t', 'Triple'), 
       ('q', 'Quad')], 
      string='Room Type'
    )

class HotelLinePackage(models.Model):
    _name = "hotel.line.package"
    
    travel_package_id = fields.Many2one(
      'travel.package', 
      string='Travel Package', 
      ondelete='cascade'
    )
    partner_id = fields.Many2one(
      'res.partner', 
      string='Hotel', 
      required=True
    )
    start_date = fields.Date(
      string='Start Date', 
      required=True
    )
    end_date = fields.Date(
      string='End Date', 
      required=True
    )
    city = fields.Char(
      related='partner_id.city', 
      string='City', 
      readonly=True
    )

class ScheduleLinePackage(models.Model):
    _name = "schedule.line.package"
    
    travel_package_id = fields.Many2one(
      comodel_name='travel.package', 
      string='Travel Package', 
      ondelete='cascade'
    )
    name = fields.Char(
      string='Name', 
      required=True
    )
    date = fields.Date(
      string='Date', 
      required=True
    )