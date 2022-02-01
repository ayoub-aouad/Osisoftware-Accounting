from odoo import models, fields,_
import openpyxl
import xlrd
import base64
import io
import csv
from odoo.exceptions import UserError, ValidationError
import datetime as dt
import pandas


class ImportJournalEntryWizard(models.TransientModel):
   _name = "import.journal.entry"

   file = fields.Binary(string="File", required=True)

   def import_journal_entry(self):
        print(self.file)
        df = pandas.io.excel.read_excel(base64.b64decode(self.file), engine='xlrd',
        dtype={'date': str,
               'Référence':str,
               'Journal':str,
               'Compte':str,
               'Intitulé':str,
               'Débit':float ,
               'Crédit': float})

        values = df['date'].values
        date = values
        values = df['Compte'].values
        compte = values
        values = df['Référence'].values
        reference = values
        values = df['Intitulé'].values
        intitule = values
        values = df['Débit'].values
        debit = values
        values = df['Crédit'].values
        credit = values
        values = df['Journal'].values
        journal = values
        
        name= reference[0]
        date = date[0]
        journal_id = self.env['account.journal'].search([('name', '=', journal[0])]).id
        self.env['account.move'].create({
        'name':name,
        'date':date,
        'journal_id' : journal_id})

        for compte,intitule, debit, credit  in zip(compte,intitule, debit, credit ):
            val = 0
            if len(str(compte)) != 8:
                raise ValidationError(_('Ce Compte " %s " ne peut pas être créé' % (compte)))
                
            
            if '.' in str(debit) :
                debit = float(debit)
            else :
                debit = 0.0
            if '.' in str(credit) :
                credit = float(credit)
            else:
                credit = 0.0
            if debit >= 0 and credit >= 0:
                if str(compte[0]) == '2' or str(compte[0]) == '3' or str(str(compte[0]) + str(compte[1])) == '51' or str(compte[0])=='6':
                    val =  float(debit) - float(credit)
                    if val >= 0:
                        debit = val
                        credit = 0.0
                    else:
                        credit = (-1)*val
                        debit= 0.0
                elif str(compte[0]) == '1' or str(compte[0]) == '4' or str(str(compte[0]) + str(compte[1])) == '55' or str(compte[0])=='7':
                    val =  float(debit) - float(credit)
                    if val >= 0:
                        debit = 0.0
                        credit = val
                    else:
                        debit = (-1)*val
                        credit= 0.0   
          
            account = self.env['account.account'].search([('code','=',compte)])
            if not account.exists():
                result = self.env['account.account'].search([('code','=',str(str(compte[0])+str(compte[1])+str(compte[2])+str(compte[3])+'0000'))])
                if result.exists():
                    account_val = [
                        {'code' : compte ,
                        'name' : intitule,
                        'reconcile' :result.reconcile ,
                        'user_type_id' : result.user_type_id.id,
                        }]
                    self.create_objects('account.account',account_val)
                    lines_val = [{'account_id' : self.env['account.account'].search([('code','=',compte)]).id,
                            'partner_id' : False,
                            'name' : intitule,
                            'tax_ids'  : False,
                            'debit'  : debit,
                            'credit': credit,
                            'tax_tag_ids' :False,
                            'tax_tag_invert':False,
                            'move_id':self.env['account.move'].search([('name','=',name),('journal_id','=',journal_id),('date','=',date)],order='id desc', limit=1).id,
                            }]
                    self.create_objects('account.move.line',lines_val)
                else:
                    raise ValidationError(_('Ce Compte " %s " n\'exist pas dans le plan comptable Maroccain, veuillez corriger votre fichier puis réessayer' % (compte)))
            else:
                
                lines_val = [{'account_id' : self.env['account.account'].search([('code','=',compte)]).id,
                        'partner_id' : False,
                        'name' : intitule,
                        'tax_ids'  : False,
                        'debit'  : debit,
                        'credit': credit,
                        'tax_tag_ids' :False,
                        'tax_tag_invert':False,
                        'move_id':self.env['account.move'].search([('name','=',name),('journal_id','=',journal_id),('date','=',date)],order='id desc', limit=1).id,
                        }]
                self.create_objects('account.move.line',lines_val)
       
            
    
                        
        


       
        
            


    
    