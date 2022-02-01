from odoo import models, fields, api, _   

class TVAObject(models.Model):
    _name = 'osi.tva'
    
    name = fields.Char(string=u"Nom",default="TVA",required=True,)
    fy_n_id = fields.Many2one('date.range', 'Exercice fiscal',copy=False,store=True,)
    line_ids = fields.One2many(comodel_name="osi.tva.line", inverse_name="tva_id", string="TVA", required=False, copy=True )
    
    @api.model
    def create(self, values):
        return super(TVAObject,self).create({
            'line_ids' : self.env['osi.tva.line'].create([{'name':'* T.V.A. Facturée','tva_id':self.id,},
                                                          {'name':'* T.V.A. Récupérable','tva_id':self.id,},
                                                          {'name':'* sur charges','tva_id':self.id,},
                                                          {'name':'* sur immobilisations','tva_id':self.id,},
                                                          {'name':'T.V.A. due ou crédit de T.V.A','tva_id':self.id,}]),})
        
    def from_string_to_list(self,val,list):
        list = []
        for x in str(val):
            list.append(x)
        return list
    
    def list_verification(self,list1,list2):

        if len(list1) == 4:
            if list1[0] == list2[0] and list1[1] == list2[1] and list1[2] == list2[2] and list1[3] == list2[3] :
                return True
        elif len(list1) == 5:
            if list1[0] == list2[0] and list1[1] == list2[1] and list1[2] == list2[2] and list1[3] == list2[3] and list1[4] == list2[4]:
                return True
        else:
            return False
        
    def import_debit_credit_per_year(self):
        for rec in self:
            journal_entries = self.env['account.move'].search([('name','!=',False),('state','=','posted')])
            item_code = []
            line_code_1 = []
            line_code_2 = []
            line_code_3 = []
            credit_4455_last = 0
            credit_4455_pre = 0
            debit_4455_last = 0
            debit_4455_pre = 0
            credit_34552_last = 0
            credit_34552_pre = 0
            debit_34552_last = 0
            debit_34552_pre = 0
            credit_34551_last = 0
            credit_34551_pre = 0
            debit_34551_last = 0
            debit_34551_pre = 0
            for entry in journal_entries:
                if rec.fy_n_id:
                    for ref in rec.fy_n_id:
                        for item in entry.line_ids:
                            item_code = rec.from_string_to_list(item.account_id.code,item_code)
                            line_code_1 = rec.from_string_to_list('4455',line_code_1)
                            line_code_2 = rec.from_string_to_list('34552',line_code_2)
                            line_code_3 = rec.from_string_to_list('34551',line_code_3)
                            if ref.date_end.year > entry.date.year:
                            
                                if rec.list_verification(line_code_1,item_code):
                                    if item.debit > 0:
                                        debit_4455_last  += item.debit
                                    if item.credit > 0 :
                                        credit_4455_last += item.credit
                                elif rec.list_verification(line_code_2,item_code):
                                    if item.debit > 0:
                                        debit_34552_last  += item.debit
                                    if item.credit > 0 :
                                        credit_34552_last += item.credit
                                elif rec.list_verification(line_code_3,item_code):
                                    if item.debit > 0:
                                        debit_34551_last  += item.debit
                                    if item.credit > 0 :
                                        credit_34551_last += item.credit
                            if ref.date_end.year == entry.date.year:
                                
                                if rec.list_verification(line_code_1,item_code):
                                    if item.debit > 0:
                                        debit_4455_pre  += item.debit
                                    if item.credit > 0 :
                                        credit_4455_pre += item.credit
                                elif rec.list_verification(line_code_2,item_code):
                                    if item.debit > 0:
                                        debit_34552_pre  += item.debit
                                    if item.credit > 0 :
                                        credit_34552_pre += item.credit
                                elif rec.list_verification(line_code_3,item_code):
                                    if item.debit > 0:
                                        debit_34551_pre  += item.debit
                                    if item.credit > 0 :
                                        credit_34551_pre += item.credit
            line_1 = self.env['osi.tva.line'].search([('name','=','* T.V.A. Facturée'),('tva_id','=',rec.id)])
            line_1.write({'start_solde':debit_4455_last - credit_4455_last,
                          'operation_solde':credit_4455_pre,
                          'declaration_solde': debit_4455_pre,
                          'end_solde':debit_4455_last - credit_4455_last + credit_4455_pre - debit_4455_pre})
            line_2 = self.env['osi.tva.line'].search([('name','=','* T.V.A. Récupérable'),('tva_id','=',rec.id)])
            line_2.write({'start_solde':debit_34552_last - credit_34552_last + debit_34551_last - credit_34551_last ,
                          'operation_solde':credit_34552_pre + credit_34551_pre,
                          'declaration_solde': debit_34552_pre + debit_34551_pre,
                          'end_solde':debit_34551_last - credit_34551_last + credit_34551_pre - debit_34551_pre + debit_34552_last - credit_34552_last + credit_34552_pre - debit_34552_pre })
            line_3 = self.env['osi.tva.line'].search([('name','=','* sur charges'),('tva_id','=',rec.id)])
            line_3.write({'start_solde':debit_34552_last - credit_34552_last,
                          'operation_solde':credit_34552_pre,
                          'declaration_solde': debit_34552_pre,
                          'end_solde':debit_34552_last - credit_34552_last + credit_34552_pre - debit_34552_pre})
            line_4 = self.env['osi.tva.line'].search([('name','=','* sur immobilisations'),('tva_id','=',rec.id)])
            line_4.write({'start_solde':debit_34551_last - credit_34551_last,
                          'operation_solde':credit_34551_pre,
                          'declaration_solde': debit_34551_pre,
                          'end_solde':debit_34551_last - credit_34551_last + credit_34551_pre - debit_34551_pre})
            line_5 = self.env['osi.tva.line'].search([('name','=','T.V.A. due ou crédit de T.V.A'),('tva_id','=',rec.id)])
            line_5.write({'start_solde':debit_4455_last - credit_4455_last - (debit_34552_last - credit_34552_last + debit_34551_last - credit_34551_last),
                          'operation_solde':credit_4455_pre - (credit_34552_pre + credit_34551_pre),
                          'declaration_solde': debit_4455_pre - (debit_34552_pre + debit_34551_pre),
                          'end_solde':debit_4455_last - credit_4455_last + credit_4455_pre - debit_4455_pre - (debit_34551_last - credit_34551_last + credit_34551_pre - debit_34551_pre + debit_34552_last - credit_34552_last + credit_34552_pre - debit_34552_pre)})
           
class TVALineObject(models.Model):
    
    _name = 'osi.tva.line'
    
    name = fields.Char(string='NATURE' ,readonly = True)
    start_solde = fields.Float(string='Solde au début de l\'exercice',readonly = True)
    operation_solde = fields.Float(string='Opérations comptables de l\'exercice',readonly = True)
    declaration_solde = fields.Float(string='Déclarations T.V.A de l\'exercice',readonly = True)
    end_solde = fields.Float(string='Solde fin d\'exercice',readonly = True)
    tva_id = fields.Many2one(comodel_name="osi.tva",)
    

