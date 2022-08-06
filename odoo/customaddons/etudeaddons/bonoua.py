# Bonoua application
from openerp import models, fields, api

class bonoua_account_analytic_line(models.Model):
    _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'

    culture = fields.Char("Culture")
    person_id = fields.Many2one("res.partner","reference")

class bonoua_res_company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    personne = fields.Many2one("res.personnes","company_id")

class bonoua_res_personnes(models.Model):
    _name = 'res.personnes'
    item_ids = fields.One2many("account.analytic.line","person_id") 
    item_id = fields.Many2one("account.analytic.line","reference")
    heure = fields.Many2one("product.uom","Heure(s)")
    nbre_jour = fields.Float(string='Nombre de jour', related='item_id.unit_amount', store=True , readonly=True)
    periode = fields.Date(string='Date de debut du projet', related='item_id.date', store=True, readonly=True)
    salaire = fields.Monetary(string="Salaire", currency_field='company_currency_id', related='item_id.amount', store=True, readonly=True)
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='SOCIETE', store=True, realondy=True)
    currency_id = fields.Many2one(related="company_id.currency_id", string="Devise", readonly=True)
    

    @api.one
    @api.depends('item_ids','item_ids.unit_amount','item_ids.amount')
    def _cal(self):
        currentci=0
        for ci in self.item_ids:
            currentci = currentci + ci.unit_amount * ci.amount * 1/240
        self.totalci = currentci

    totalci = fields.Monetary(string="Salaire Net", currency_field='company_currency_id', readonly=True, store=True,compute="_cal")    
       
    







