""" init py report account.report.esg.caf """

from odoo import models, api, _


# pylint: disable=no-member, unused-argument, consider-using-ternary
# pylint: disable=no-self-use, unused-variable, redefined-outer-name
# pylint: disable=too-many-arguments, too-many-locals, protected-access
# pylint: disable=too-many-nested-blocks
class AccountReportEGSCAF(models.AbstractModel):
    """ init py report account.report.esg.caf """
    _name = "account.report.esg.caf"
    _description = "account.report.esg.caf"
    _inherit = "account.report.esg.tfr"
    _group_model = 'esg.caf.group'

    @api.model
    def _get_report_name(self):
        """
        Override  _get_report_name
        """
        return _("ESG CAF")
