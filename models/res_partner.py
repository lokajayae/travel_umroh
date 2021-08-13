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
  age = fields.Integer(
      string = "Umur",
      compute = "_compute_age",
      store = True,
      readonly = True
  )
  date_of_birth = fields.Date(
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

  @api.depends('date_of_birth')
  def _compute_age(self) :
    today = fields.Date.today()
    difference = 0

    for people in self :
      if people.date_of_birth :
        # if date of birth from a person is exist
        if people.date_of_birth.month < today.month :
          difference = 0
        elif people.date_of_birth.month == today.month :
          if people.date_of_birth.day <= today.day :
            difference = 0
          elif people.date_of_birth.day > today.day :
            difference = -1
          else :
            difference = -1
          
        people.age = today.year - people.date_of_birth.year + difference
      else :
        # if date of birth is not exist
        people.age = -1


    