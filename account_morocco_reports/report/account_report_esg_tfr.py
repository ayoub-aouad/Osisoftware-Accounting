""" init py report account.report.profit """

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.tools.misc import format_date


# pylint: disable=no-member, unused-argument, consider-using-ternary
# pylint: disable=no-self-use, unused-variable, redefined-outer-name
# pylint: disable=too-many-arguments, too-many-locals, protected-access
# pylint: disable=too-many-nested-blocks
class AccountReportEsgTFR(models.AbstractModel):
    """ init py report account.report.esg.tfr """
    _name = "account.report.esg.tfr"
    _description = "account.report.esg.tfr"
    _inherit = "account.report.profit"
    _group_model = 'esg.tfr.group'

    @api.model
    def _get_templates(self):
        """
        Override function _get_templates
        """
        templates = super(AccountReportEsgTFR, self)._get_templates()
        templates['main_template'] = 'account_morocco_reports.' \
                                     'morocco_main_template'
        templates['search_template'] = 'account_morocco_reports.' \
                                       'search_template_profit'
        return templates

    @api.model
    def _get_columns_name(self, options):
        """
        Override function _get_columns_name
        """
        columns = [{'name': '', 'style': 'width:2%'},
                   {'name': '', 'style': 'width:80%'},
                   {'name': _('Exercice'), 'class': 'number'},
                   {'name': _('Exercice Précédent'), 'class': 'number'},
                   {'name': _('Net'), 'class': 'number '}, ]
        count_opt = len(options['comparison']['periods'])
        if options.get('comparison') and options['comparison'].get('periods'):
            columns += [{'name': _('Net'), 'class': 'number '}] * count_opt
        return columns

    
    @api.model
    def _get_report_name(self):
        """
        Override  _get_report_name
        """
        return _("ESG TFR")
