import time
from odoo.report import report_sxw
 
class custom_laporan(report_sxw.rml_parse):
  def __init__(self, cr, uid, name, context):
    super(custom_laporan, self).__init__(cr, uid, name, context=context)
    self.localcontext.update({
    'time': time
    })
    
    report_sxw.report_sxw(
      'report.surat.jalan', 
      'stock.picking', 
      'addons/travel_umroh/report/surat_jalan.rml', 
      parser=custom_laporan, 
      header=False)
