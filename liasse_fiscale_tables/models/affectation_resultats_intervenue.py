# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AffectationResultatsIntervenue(models.Model):
    _name = 'affectation.resultats.intervenue'
    _description = 'AFFECTATION DES RESULTATS INTERVENUE'

    name = fields.Char(string=u"Nom",default="ETAT D'AFFECTATION DES RESULTATS INTERVENUE AU COURS DE L'EXERCICE",required=True,)
    fy_n_id = fields.Many2one('date.range', 'Exercice fiscal',copy=False,store=True,)
    affectation_resultats_intervenue_line1_ids = fields.One2many(comodel_name="affectation.resultats.intervenue.line1", inverse_name="affectation_resultats_intervenue_id", string="ORIGINE DES RESULTATS A AFFECTER", required=False, copy=True )
    affectation_resultats_intervenue_line2_ids = fields.One2many(comodel_name="affectation.resultats.intervenue.line2", inverse_name="affectation_resultats_intervenue_id", string="AFFECTATION DES RESULTATS", required=False, copy=True )

    _sql_constraints = [
        ('unique_fy', 'UNIQUE(fy_n_id)', 'Un autre tableau existe pour le meme exercice!'),
    ]
    

    @api.model
    def create(self, values):
        return super(AffectationResultatsIntervenue,self).create({
            'affectation_resultats_intervenue_line1_ids' : self.env['affectation.resultats.intervenue.line1'].create([{'name':'Décision du (Date AGOA ....)','code':'','affectation_resultats_intervenue_id':self.id,},
                                                                  {'name':'Report à nouveau (Antérieur) + ou(-)','code':'116','affectation_resultats_intervenue_id':self.id,},
                                                                  {'name':'Résultat net en instance d\'affectation + ou(-)','code':'118','affectation_resultats_intervenue_id':self.id,},
                                                                  {'name':'Résultat net de l\'exercice + ou(-)','code':'119','affectation_resultats_intervenue_id':self.id,},
                                                                  {'name':'Prélèvement sur les réserves +','code':'115','affectation_resultats_intervenue_id':self.id,},
                                                                  {'name':'Autres prélèvements +','code':'','affectation_resultats_intervenue_id':self.id,}]),
            'affectation_resultats_intervenue_line2_ids' : self.env['affectation.resultats.intervenue.line2'].create([{'name':'Réserve Légale','code':'1140','affectation_resultats_intervenue_id':self.id,},
                                                                  {'name':'Autres réserves ','code':'115','affectation_resultats_intervenue_id':self.id,},
                                                                  {'name':'Tantièmes (Abrogé)','code':'4465','affectation_resultats_intervenue_id':self.id,},
                                                                  {'name':'Dividendes (Mt Brut)(1)','code':'4465','affectation_resultats_intervenue_id':self.id,},
                                                                  {'name':'Autres affectation','code':'','affectation_resultats_intervenue_id':self.id,},
                                                                  {'name':'Report à nouveau reportable','code':'116','affectation_resultats_intervenue_id':self.id,}]),
        })

    def from_string_to_list(self,val,list):
        list = []
        for x in str(val):
            list.append(x)
        return list
    
    def list_verification(self,list1,list2):
        if len(list1) == 2:
            if list1[0] == list2[0] and list1[1] == list2[1] :
                return True
        if len(list1) == 3:
            if list1[0] == list2[0] and list1[1] == list2[1] and list1[2] == list2[2] :
                return True
        elif len(list1) == 4:
            if list1[0] == list2[0] and list1[1] == list2[1] and list1[2] == list2[2] and list1[3] == list2[3] :
                return True
        else:
            return False

            



    def import_debit_credit_per_year(self):
        for rec in self:
            journal_entries = self.env['account.move'].search([('name','!=',False),('state','=','posted')])
            if rec.affectation_resultats_intervenue_line1_ids:
                for line in rec.affectation_resultats_intervenue_line1_ids:
                    initial_balance = 0
                    item_code = []
                    line_code = []
                    for entry in journal_entries:
                        if rec.fy_n_id:
                            for ref in rec.fy_n_id:
                                if ref.date_end.year > entry.date.year:
                                    for item in entry.line_ids:
                                        item_code = rec.from_string_to_list(item.account_id.code,item_code)
                                        line_code = rec.from_string_to_list(line.code,line_code)
                                        if rec.list_verification(line_code,item_code):
                                            if item.debit > 0:
                                                initial_balance  += item.debit
                                            if item.credit > 0 :
                                                initial_balance -= item.credit
                    line.montant = initial_balance
                for line in rec.affectation_resultats_intervenue_line2_ids:
                    end_balance = 0
                    item_code = []
                    line_code = []
                    for entry in journal_entries:
                        if rec.fy_n_id:
                            for ref in rec.fy_n_id:
                                if ref.date_end.year >= entry.date.year:
                                    for item in entry.line_ids:
                                        item_code = rec.from_string_to_list(item.account_id.code,item_code)
                                        line_code = rec.from_string_to_list(line.code,line_code)
                                        if rec.list_verification(line_code,item_code):
                                            if item.debit > 0:
                                                end_balance  += item.debit 
                                            if item.credit > 0 :
                                                end_balance -= item.credit 
                    line.montant = end_balance 
                    

class AffectationResultatsIntervenueLine1(models.Model):
    _name = 'affectation.resultats.intervenue.line1'
    _description = 'LIGNES AFFECTATION DES RESULTATS INTERVENUE 1'

    name = fields.Char(string=u"Nom, prénoms ou raison sociale des principaux associés",required=True,readonly=True)
    code = fields.Char(string=u"Code", required=False, )
    montant = fields.Float(string=u"Montant",  required=False, )
    affectation_resultats_intervenue_id = fields.Many2one(comodel_name="affectation.resultats.intervenue", string="AFFECTATION DES RESULTATS INTERVENUE", required=False, )


class AffectationResultatsIntervenueLine2(models.Model):
    _name = 'affectation.resultats.intervenue.line2'
    _description = 'LIGNES AFFECTATION DES RESULTATS INTERVENUE 2'

    name = fields.Char(string=u"Nom, prénoms ou raison sociale des principaux associés",required=True,readonly=True)
    code = fields.Char(string=u"Code", required=False, )
    montant = fields.Float(string=u"Montant",  required=False, )
    affectation_resultats_intervenue_id = fields.Many2one(comodel_name="affectation.resultats.intervenue", string="AFFECTATION DES RESULTATS INTERVENUE", required=False, )
