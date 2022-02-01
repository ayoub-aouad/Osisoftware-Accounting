""" init py report account.report.loss """

from odoo import models, api, _


# pylint: disable=no-member, unused-argument, consider-using-ternary
# pylint: disable=no-self-use, unused-variable, redefined-outer-name
# pylint: disable=too-many-arguments, too-many-locals, protected-access
# pylint: disable=too-many-nested-blocks
class AccountReportLoss(models.AbstractModel):
    """ init py report account.report.loss """
    _name = "account.report.loss"
    _description = "account.report.loss"
    _inherit = "account.report.profit"
    _group_model = 'loss.group'

    @api.model
    def _get_report_name(self):
        """
        Override  _get_report_name
        """
        return _("Profit and Loss Part 2")
