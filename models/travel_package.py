from io import BytesIO
from odoo import models, fields, api
import base64
import xlsxwriter

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
    filename = fields.Char(
      string='Filename'
    )
    data_file = fields.Binary(
      string='Data file'
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
    
    def print_xls_participant(self) :
      # Membuat worksheet
      file_name = "Daftar Jamaah - " + str(self.name) + ".xlsx"
      file_data = BytesIO()
      workbook = xlsxwriter.Workbook(file_data)
      ws = workbook.add_worksheet("Daftar Jamaah")

      # Menambah Style Worksheet
      style = workbook.add_format({'left': 1, 'top': 1,'right':1,'bold': True,'fg_color': '#339966','font_color': 'white','align':'center'})
      style.set_text_wrap()
      style.set_align('vcenter')
      style_bold = workbook.add_format({'left': 1, 'top': 1,'right':1,'bottom':1,'bold': True,'align':'center','num_format':'_(Rp* #,##0_);_(Rp* (#,##0);_(* "-"??_);_(@_)'})
      style_bold_orange = workbook.add_format({'left': 1, 'top': 1,'right':1,'bold': True,'align':'center','fg_color': '#FF6600','font_color': 'white'})
      style_no_bold = workbook.add_format({'left': 1,'right':1,'bottom':1, 'num_format':'_(Rp* #,##0_);_(Rp* (#,##0);_(* "-"??_);_(@_)'})
      
      # Configure Column Width
      ws.set_column(0, 0, 10) # Column A
      ws.set_column(1, 2, 15) # Column B - C
      ws.set_column(3, 3, 30) # Column D
      ws.set_column(4, 5, 15) # Column E - F
      ws.set_column(6, 10, 20) # Column G - K
      ws.set_column(11, 11, 30) # Column L

      # Write Title
      ws.write(1, 2, 'MANIFEST', style_bold)
      ws.write(1, 3, self.name, style_no_bold)

      # Write Header Jamaah
      ws.write(3, 0, 'NUMBER', style_bold_orange)
      ws.write(3, 1, 'TITLE', style_bold_orange)
      ws.write(3, 2, 'GENDER', style_bold_orange)
      ws.write(3, 3, 'FULL NAME', style_bold_orange)
      ws.write(3, 4, 'BIRTH PLACE', style_bold_orange)
      ws.write(3, 5, 'DATE OF BIRTH', style_bold_orange)
      ws.write(3, 6, 'PASSPORT NUMBER', style_bold_orange)
      ws.write(3, 7, 'PASSPOR ISSUED', style_bold_orange)
      ws.write(3, 8, 'PASSPORT EXPIRED', style_bold_orange)
      ws.write(3, 9, 'IMMIGRATION', style_bold_orange)
      ws.write(3, 10, 'AGE', style_bold_orange)
      ws.write(3, 11, 'NIK', style_bold_orange)
      ws.write(3, 12, 'ORDER', style_bold_orange)
      ws.write(3, 13, 'ROOM TYPE', style_bold_orange)
      ws.write(3, 14, 'ROOM LEADER', style_bold_orange)
      ws.write(3, 15, 'ROOM NUMBER', style_bold_orange)
      ws.write(3, 16, 'ADDRESS', style_bold_orange)
      
      last_row = 4
      jamaah_count = 1

      # Write Data Jamaah
      for participant in self.participant_line:
        passport = self.env['sale.passport.line'].search([('partner_id', '=', participant.partner_id.id)])
        ws.write(last_row, 0, str(jamaah_count), style_no_bold)
        ws.write(last_row, 1, participant.partner_id.title.display_name, style_no_bold)
        ws.write(last_row, 2, participant.partner_id.gender, style_no_bold)
        ws.write(last_row, 3, participant.partner_id.name, style_no_bold)
        ws.write(last_row, 4, participant.partner_id.birth_place, style_no_bold)
        ws.write(last_row, 5, participant.partner_id.date_of_birth, style_no_bold)
        ws.write(last_row, 6, str(passport.passport_number), style_no_bold)
        ws.write(last_row, 7, participant.partner_id.city, style_no_bold)
        ws.write(last_row, 8, passport.expiry, style_no_bold)
        ws.write(last_row, 9, passport.issued, style_no_bold)
        ws.write(last_row, 10, str(participant.partner_id.age), style_no_bold)
        ws.write(last_row, 11, str(participant.partner_id.identity_number), style_no_bold)
        last_row += 1
        jamaah_count += 1

      # Write Header Airline
      
      # Write Data Airline
      
      # Close Workbook
      workbook.close()
      out = base64.encodestring(file_data.getvalue())
      self.write({
        'data_file' : out,
        "filename" : file_name
      })

      # base_url = self.env['ir.config_parameter'].get_param('web.base.url')
      # attachment_obj = self.env['ir.attachment']

      # attachment_id = attachment_obj.create({
      #   'name': file_name, 
      #   'datas_fname': 'xlsx', 
      #   'datas': out
      # })

      # download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
      
      # return {
      #   "type": "ir.actions.act_url",
      #   "url": str(base_url) + str(download_url),
      #   "target": "new",
      # }


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