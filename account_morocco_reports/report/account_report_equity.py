""" init py report account.report.equity """

from odoo import models, api, _


# pylint: disable=no-member, unused-argument, consider-using-ternary
# pylint: disable=no-self-use, unused-variable, redefined-outer-name
# pylint: disable=too-many-arguments, too-many-locals, protected-access
# pylint: disable=too-many-nested-blocks
class AccountReportEquity(models.AbstractModel):
    """ init py report account.report.equity """
    _name = "account.report.equity"
    _description = "account.report.equity"
    _inherit = "account.report.assets"
    _group_model = 'equity.group'
    _number_of_columns = 1

    @api.model
    def _get_templates(self):
        """
        Override function _get_templates
        """
        templates = super(AccountReportEquity, self)._get_templates()
        templates['main_template'] = 'account_morocco_reports.' \
                                     'morocco_main_template'
        templates['main_table_header_template'] = 'account_morocco_reports.' \
                                                  'template_equity_table_header'
        return templates

    @api.model
    def _get_super_columns(self, options):
        """
        Override _get_super_columns
        """
        date_cols = options.get('date') and [options['date']] or []
        date_cols += (options.get('comparison') or {}).get('periods', [])
        columns = []
        columns += date_cols
        return {'columns': columns, 'x_offset': 1, 'merge': 1}

    @api.model
    def _get_columns_name(self, options):
        """
        Override function _get_columns_name
        """
        columns = [
            {'name': '', 'style': 'width:2%'},
            {'name': '', 'style': 'width:80%'},
            {'name': _('Net'), 'class': 'number '},
        ]
        count_opt = len(options['comparison']['periods'])
        if options.get('comparison') and options['comparison'].get('periods'):
            columns += [{'name': _('Net'), 'class': 'number '}] * count_opt
        return columns

    @api.model
    def _get_report_name(self):
        """
        Override  _get_report_name
        """
        return _("Morocco Report Equity")
