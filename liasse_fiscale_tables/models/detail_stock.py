# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DetailStock(models.Model):
    _name = 'detail.stock'
    _description = 'Detail Stock'

    name = fields.Char(string=u"Nom",default="ETAT DETAIL DES STOCKS",required=True,)
    fy_n_id = fields.Many2one('date.range', 'Exercice fiscal',copy=False)
    detail_stock_line_ids = fields.One2many(comodel_name="detail.stock.line", inverse_name="detail_stock_id", string="Lignes", required=False, copy=True, )

    _sql_constraints = [
        ('unique_fy', 'UNIQUE(fy_n_id)', 'Un autre tableau existe pour le meme exercice!'),
    ]
    
    
    @api.model
    def create(self, values):
        return super(DetailStock,self).create({
            'detail_stock_line_ids' : self.env['detail.stock.line'].create([{'name':'Biens Immeubles','code_1':'3111','code_2':'39111','detail_stock_id':self.id,},
                                                                  {'name':'Biens Meubles','code_1':'3112','code_2':'39112','detail_stock_id':self.id,},
                                                                  {'name':'Matière Premières','code_1':'31212','code_2':'391222','detail_stock_id':self.id,},
                                                                  {'name':'Matières Consommables','code_1':'31222','code_2':'391222','detail_stock_id':self.id,},
                                                                  {'name':'Pièces Détachées','code_1':'31226/31227','code_2':'391226/391227','detail_stock_id':self.id,},
                                                                  {'name':'Carburants, Lubrifiants Pour Véhicules de transport','code_1':'31223/31224','code_2':'391223/391224','detail_stock_id':self.id,},
                                                                  {'name':'Récupérables','code_1':'31233','code_2':'391233','detail_stock_id':self.id,},
                                                                  {'name':'Vendus','code_1':'31232','code_2':'391232','detail_stock_id':self.id,},
                                                                  {'name':'Perdus','code_1':'31231','code_2':'391231','detail_stock_id':self.id,},
                                                                  {'name':'Produits En cours','code_1':'3131/3138/314','code_2':'39131/3914','detail_stock_id':self.id,},
                                                                  {'name':'Etudes En cours','code_1':'31342','code_2':'391342','detail_stock_id':self.id,},
                                                                  {'name':'Travaux En-cours','code_1':'31341','code_2':'391341','detail_stock_id':self.id,},
                                                                  {'name':'Services En-cours','code_1':'31343','code_2':'391343','detail_stock_id':self.id,},
                                                                  {'name':'Produits Finis','code_1':'3151/3152','code_2':'3915/39151/39152','detail_stock_id':self.id,},
                                                                  {'name':'Biens Finis','code_1':'3156/3158','code_2':'39156/39158','detail_stock_id':self.id,},
                                                                  {'name':'Déchets','code_1':'31451','code_2':'391451','detail_stock_id':self.id,},
                                                                  {'name':'Rebuts','code_1':'31452','code_2':'391452','detail_stock_id':self.id,},
                                                                  {'name':'Matières de Récupération','code_1':'31453','code_2':'391453','detail_stock_id':self.id,}]),})
     
     # this function convert string of codes to list     
    def from_string_to_list(self,val,list):
        list = []
        for x in str(val):
            list.append(x)
        return list
    
    # this functtion verify list elements
    def list_verification(self,list1,list2):
        if len(list1) == 4:
            if list1[0] == list2[0] and list1[1] == list2[1] and list1[2] == list2[2] and list1[3] == list2[3] :
                return True
        elif len(list1) == 5:
            if list1[0] == list2[0] and list1[1] == list2[1] and list1[2] == list2[2] and list1[3] == list2[3] and list1[4] == list2[4] :
                return True
        elif len(list1) == 6:
            if list1[0] == list2[0] and list1[1] == list2[1] and list1[2] == list2[2] and list1[3] == list2[3] and list1[4] == list2[4] and list1[5] == list2[5]:
                return True
        else:
            return False
    
    # this function verified lines that contains multiple codes
    def verifiy_list_length(self,list,item_code,line_code_1_1= [],line_code_1_2= [],line_code_1_3= [],line_code_2_1= [],line_code_2_2= [],line_code_2_3 = []):
        for rec in self:
            if len(list) == 2:
                line_code_1_1 = rec.from_string_to_list(list[0],line_code_1_1)
                line_code_1_2 = rec.from_string_to_list(list[1],line_code_1_2)
                if  rec.list_verification(line_code_1_1,item_code) or rec.list_verification(line_code_1_2,item_code):
                    return True
            elif len(list) ==3:
                line_code_1_1 = rec.from_string_to_list(list[0],line_code_1_1)
                line_code_1_2 = rec.from_string_to_list(list[1],line_code_1_2)
                line_code_1_3 = rec.from_string_to_list(list[2],line_code_1_3)
                if  rec.list_verification(line_code_1_1,item_code) or rec.list_verification(line_code_1_2,item_code) or rec.list_verification(line_code_1_3,item_code):
                    return True
            
            else:
                return False

    # this function import and calculates debit and credit for each line
    def import_debit_credit_per_year(self):
        for rec in self :
            journal_entries = self.env['account.move'].search([('name','!=',False),('state','=','posted')])
            if rec.detail_stock_line_ids:  
                for line in rec.detail_stock_line_ids:
                    list_1 = []
                    list_2 = []
                    item_code = []
                    line_code_1 = []
                    line_code_2 = []
                    initial_brut = 0
                    initial_pro = 0
                    end_brut = 0
                    end_pro = 0
                    for entry in journal_entries:
                        if '/' in line.code_1 or '/' in line.code_2:
                            list_1 = line.code_1.split('/')
                            list_2 = line.code_2.split('/')
                            if rec.fy_n_id.date_end.year > entry.date.year:
                                for item in entry.line_ids:
                                    item_code = rec.from_string_to_list(item.account_id.code,item_code)
                                    
                                    if rec.verifiy_list_length(list_1,item_code,line_code_1_1= [],line_code_1_2= [],line_code_1_3= [],line_code_2_1= [],line_code_2_2= [],line_code_2_3 = []):
                                        if item.debit > 0:
                                            initial_brut  += item.debit
                                        if item.credit > 0 :
                                            initial_brut -= item.credit
                                    if rec.verifiy_list_length(list_2,item_code,line_code_1_1= [],line_code_1_2= [],line_code_1_3= [],line_code_2_1= [],line_code_2_2= [],line_code_2_3 = []):
                                        if item.debit > 0:
                                            initial_pro  += item.debit
                                        if item.credit > 0 :
                                            initial_pro -= item.credit
                            elif rec.fy_n_id.date_end.year == entry.date.year:
                                for item in entry.line_ids:
                                    item_code = rec.from_string_to_list(item.account_id.code,item_code)
                                    if rec.verifiy_list_length(list_1,item_code,line_code_1_1= [],line_code_1_2= [],line_code_1_3= [],line_code_2_1= [],line_code_2_2= [],line_code_2_3 = []):
                                        if item.debit > 0:
                                            end_brut  += item.debit
                                        if item.credit > 0 :
                                            end_brut -= item.credit
                                    if rec.verifiy_list_length(list_2,item_code,line_code_1_1= [],line_code_1_2= [],line_code_1_3= [],line_code_2_1= [],line_code_2_2= [],line_code_2_3 = []):
                                        if item.debit > 0:
                                            end_pro  += item.debit
                                        if item.credit > 0 :
                                            end_pro -= item.credit
                        else:
                            if rec.fy_n_id.date_end.year > entry.date.year:
                                for item in entry.line_ids:
                                    item_code = rec.from_string_to_list(item.account_id.code,item_code)
                                    line_code_1 = rec.from_string_to_list(line.code_1,line_code_1)
                                    line_code_2 = rec.from_string_to_list(line.code_2,line_code_2)
                                    if rec.list_verification(line_code_1,item_code):
                                        if item.debit > 0:
                                            initial_brut  += item.debit
                                        if item.credit > 0 :
                                            initial_brut -= item.credit
                                    if rec.list_verification(line_code_2,item_code):
                                        if item.debit > 0:
                                            initial_pro  += item.debit
                                        if item.credit > 0 :
                                            initial_pro -= item.credit
                            elif rec.fy_n_id.date_end.year == entry.date.year:
                                for item in entry.line_ids:
                                    item_code = rec.from_string_to_list(item.account_id.code,item_code)
                                    line_code_1 = rec.from_string_to_list(line.code_1,line_code_1)
                                    line_code_2 = rec.from_string_to_list(line.code_2,line_code_2)
                                    if rec.list_verification(line_code_1,item_code):
                                        if item.debit > 0:
                                            end_brut  += item.debit 
                                        if item.credit > 0 :
                                            end_brut -= item.credit 
                                    if rec.list_verification(line_code_2,item_code):
                                        if item.debit > 0:
                                            end_pro  += item.debit
                                        if item.credit > 0 :
                                            end_pro -= item.credit
                    line.montant_brut_stock_initial = initial_brut
                    line.provisions_stock_initial = initial_pro
                    line.provisions_stock_final = end_pro + initial_pro
                    line.montant_brut_stock_final = end_brut + initial_brut
        
    


class DetailStockLine(models.Model):
    _name = 'detail.stock.line'
    _description = 'LIGNES Detail Stock'

    name = fields.Char(string=u"Stock",required=True,)
    # fy_n_id = fields.Many2one('date.range', 'Exercice fiscal')
    code_1 = fields.Char(string=u"Code 1", required=True, )
    code_2 = fields.Char(string=u"Code 2", required=True, )
    montant_brut_stock_final = fields.Float(string=u"Montant brut Final",  required=False, )
    provisions_stock_final = fields.Float(string=u"Provision pour dépréciation Final",  required=False, )
    montant_net_stock_final = fields.Float(string=u"Montant net Final",  required=False, )
    montant_brut_stock_initial = fields.Float(string=u"Montant brut Initial",  required=False, )
    provisions_stock_initial = fields.Float(string=u"Provision pour dépréciation Initial",  required=False, )
    montant_net_stock_initial = fields.Float(string=u"Montant net Initial",  required=False, )
    variation_stock = fields.Float(string=u"Variation de stock",  required=False, store=True, compute='compute_last_line')
    detail_stock_id = fields.Many2one(comodel_name="detail.stock", string=u"Detail Stock", required=False, )
    
    @api.depends('montant_net_stock_initial','montant_net_stock_final')
    def compute_last_line(self):
        for rec in self:
            rec.variation_stock = rec.montant_net_stock_initial - rec.montant_net_stock_final
            return rec.variation_stock
        