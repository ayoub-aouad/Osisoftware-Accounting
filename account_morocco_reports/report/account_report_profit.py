""" init py report account.report.profit """

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.tools.misc import format_date


# pylint: disable=no-member, unused-argument, consider-using-ternary
# pylint: disable=no-self-use, unused-variable, redefined-outer-name
# pylint: disable=too-many-arguments, too-many-locals, protected-access
# pylint: disable=too-many-nested-blocks
class AccountReportProfit(models.AbstractModel):
    """ init py report account.report.profit """
    _name = "account.report.profit"
    _description = "account.report.profit"
    _inherit = "account.report.assets"
    _group_model = 'profit.group'

    filter_date = {'mode': 'range', 'filter': 'this_year',
                   'date_from': fields.Date.to_string(
                       datetime.now().replace(month=1, day=1))}

    def _get_date_from(self, options, period_fiscal_year=None):
        """
        Get Date From
        :return:
        """
        if options and options.get('date'):
            if period_fiscal_year:
                date_to = options.get('date').get('date_to')
                return self._get_from_fiscal_year(date_to)[1]
            return options and options.get('date').get('date_from')
        return '1900-01-01'

    @api.model
    def _get_templates(self):
        """
        Override function _get_templates
        """
        templates = super(AccountReportProfit, self)._get_templates()
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
                   {'name': _('Current Year'), 'class': 'number'},
                   {'name': _('Previous Year'), 'class': 'number'},
                   {'name': _('Net'), 'class': 'number '}, ]
        count_opt = len(options['comparison']['periods'])
        if options.get('comparison') and options['comparison'].get('periods'):
            columns += [{'name': _('Net'), 'class': 'number '}] * count_opt
        return columns

    @api.model
    def _get_dates_period(self, options, date_from, date_to, mode,
                          period_type=None, strict_range=False):
        """
        Override _get_dates_period
        """
        super(AccountReportProfit, self)._get_dates_period(
            options, date_from, date_to, mode, period_type=period_type,
            strict_range=strict_range
        )
        dt_from_str = format_date(self.env, fields.Date.to_string(date_from))
        dt_to_str = format_date(self.env, fields.Date.to_string(date_to))
        string = _('Form %s To %s') % (dt_from_str, dt_to_str)
        return {
            'string': string,
            'period_type': 'year',
            'mode': 'range',
            'strict_range': strict_range,# i add this line
            'date_from': fields.Date.to_string(date_from),
            'date_to': fields.Date.to_string(date_to),
        }

    @api.model
    def _get_options(self, previous_options=None):
        """
        Override _get_options
        """
        res = super(AccountReportProfit, self)._get_options(
            previous_options=previous_options)
        dateto_datetime = datetime.strptime(res['date']['date_to'], "%Y-%m-%d")
        count_opt = res['comparison']['number_period']
        comparison_filter = res['comparison']['filter']
        if comparison_filter == 'previous_period':
            periods = []
            for index in range(1, count_opt + 1):
                x_dateto = dateto_datetime - relativedelta(years=index)
                x_datefrom = x_dateto.replace(day=1, month=1)
                dt_to_str = format_date(self.env, x_dateto)
                dt_from_str = format_date(self.env, x_datefrom)
                string = _('From %s To %s ') % (dt_from_str, dt_to_str)
                periods.append({
                    'string': string,
                    'period_type': 'year',
                    'mode': 'range',
                    'date_from': res['date']['date_from'],
                    'date_to': fields.Date.to_string(x_dateto),
                })
            res['comparison']['periods'] = periods
        return res

    def _set_context(self, options):
        """
        _set_context
        """
        ctx = super(AccountReportProfit, self)._set_context(options)
        ctx['date_from'] = options['date']['date_from']
        ctx['date_to'] = options['date']['date_to']
        return ctx

    @api.model
    def _get_report_name(self):
        """
        Override  _get_report_name
        """
        return _("Profit and Loss Part 1")
