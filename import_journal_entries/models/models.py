# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveInheritance(models.Model):
    _inherit = 'account.move'

    def _check_balanced(self):
        return True
