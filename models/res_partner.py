from odoo import models, fields, api, _
from odoo.exceptions import UserError

class NamaModel(models.Model):
  _inherit = 'res.partner'

  identity_number = fields.Char(
    string="KTP Number"
  )
  father_name = fields.Char(
    string="Father's Name"
  )
  mother_name = fields.Char(
    string="Mother's Name"
  )
  birth_place = fields.Char(
    string = "Birth Place"
  )
  date_of_birth = fields.Char(
    string="Date of Birth"
  )
  blood_type = fields.Selection(
    [("a", "A"),
     ("b", "B"),
     ("ab", "AB"),
     ("o", "O")],
    string="Blood Type")
  gender = fields.Selection(
    [("male", "Male"),
     ("female", "Female")],
     string="Gender"
  )
  marital_status = fields.Selection(
    [("single", "Single"),
     ("married", "Married"),
     ("divorce", "Divorce")],
    string="Marital Status"
  )


    