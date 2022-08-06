# Entreprise application
from openerp import models, fields, api

class Entreprise_res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    banq = fields.Many2one("res.bank","Banque")
    occas = fields.Char("Entite morale")

class Entreprise_res_personnes(models.Model):
    _name = 'res.personnes'
    name = fields.Char("Nom")
    phone = fields.Char("Telephone")
    pers = fields.Char("Personne morale")
    date = fields.Date("Date")

class Entreprise_res_planift(models.Model):
    _name = 'res.planift'
    place = fields.Char("A mettre en place")
    note = fields.Text("Note")
    tache = fields.Datetime("Date du jour")
    tach = fields.Char("Tache du jour")
    name = fields.Many2one("res.users","Nom")
    demarche = fields.Char("Demarches administratives")
    mail = fields.Char("Email a envoyer")

class Entreprise_res_fraisdt(models.Model):
    _name = 'res.fraisdt'
    comp_kilo = fields.Integer("Compteur Kilometrique")
    date_frais = fields.Date("Date de frais deplacement du mois")
    km = fields.Float("Kilometrique")
    materiel = fields.Many2one("product.product","Materiel")
    observation = fields.Text("Observations")
    parcours = fields.Char("Parcours")
    vehicule = fields.Char("Vehicule")

class Entreprise_res_suivist(models.Model):
    _name = 'res.suivist'
    Suivist_id = fields.Many2one("res.personnes","Nom Commercial")
    ca1 = fields.Float("Chiffre d'affaire_1")
    ca2 = fields.Float("Chiffre d'affaire_2")
    ca3 = fields.Float("Chiffre d'affaire_3")
    ca4 = fields.Float("Chiffre d'affaire_4")
    ca5 = fields.Float("Chiffre d'affaire_5")
    ca6 = fields.Float("Chiffre d'affaire_6")
    ca7 = fields.Float("Chiffre d'affaire_7")
    ca8 = fields.Float("Chiffre d'affaire_8")
    ca9 = fields.Float("Chiffre d'affaire_9")
    ca10 = fields.Float("Chiffre d'affaire_10")
    date_mois = fields.Date("Date du mois")

class Entreprise_res_suivistitem(models.Model):
    _name = 'res.suivistitem'
    suivi_ids = fields.One2many("res.suivist","Suivist_id")
    date_mois = fields.Date("Jour du mois")

    @api.one
    @api.depends('suivi_ids','suivi_ids.ca1','suivi_ids.ca2','suivi_ids.ca3','suivi_ids.ca4','suivi_ids.ca5','suivi_ids.ca6','suivi_ids.ca7','suivi_ids.ca8','suivi_ids.ca9','suivi_ids.ca10')
    def _calcu(self):
        currentca=0
        for ca in self.suivi_ids:
            currentca = currentca + ca.ca1 + ca.ca2 + ca.ca3 + ca.ca4 + ca.ca5 + ca.ca6 + ca.ca7 + ca.ca8 + ca.ca9 + ca.ca10
        self.totalca = currentca

    totalca = fields.Float(string="Total chiffre d'affaire", store=True, compute="_calcu")

class Entreprise_res_detaict(models.Model):
    _name = 'res.detaict'
    date = fields.Date("Date")
    materiel = fields.Many2one("product.product","Ordinateur")
    peripherique = fields.Char("Peripherique")
    equi = fields.Char("Autres equipements Informatiques")

class Entreprise_res_bord1(models.Model):
    _name = 'res.bord1'
    bordor_id = fields.Many2one("res.personnes","Nom livreur")
    prix = fields.Integer("Prix Unitaire")
    quanti = fields.Integer("Quantite de materiel")
    
class Entreprise_res_bord(models.Model):
    _name = 'res.bord'
    date_commande = fields.Datetime("Date_commande")
    prix_unitaire = fields.Integer(string="Prix Unitaire", related="bordo_ids.prix", store=True, readonly=True)
    reference_bon_commande = fields.Many2one("sale.order","Reference bon de commande")
    reference_client = fields.Many2one("res.partner","Reference Client")
    reference_facture = fields.Many2one("account.invoice","Reference Facture")
    reference_materiel = fields.Many2one("product.product","Reference de materiel")
    bordo_ids = fields.One2many("res.bord1","bordor_id")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='SOCIETE')
    currency_id = fields.Many2one(related="company_id.currency_id", string="Devise", readonly=True)

    @api.one
    @api.depends('bordo_ids','bordo_ids.prix','bordo_ids.quanti')
    def _calcuo(self):
        currentbor=0
        for bor in self.bordo_ids:
            currentbor = currentbor + bor.prix * bor.quanti
        self.totalbor = currentbor

    totalbor = fields.Integer(string="Total", store=True, compute="_calcuo")

class Entreprise_res_calcul_marge(models.Model):
    _name = 'res.calcul.marge'
    prixacha = fields.Float(string="Prix Achat")
    prixven = fields.Float(string="Prix Vente")
    materiel =  fields.Many2one("product.product","Materiel")
    Calculer_id = fields.Many2one("res.personnes","Nom Commercial")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='SOCIETE')
    currency_id = fields.Many2one(related="company_id.currency_id", string="Devise", readonly=True)

class Entreprise_res_calculitem(models.Model):
    _name = 'res.calculitem'
    margetotal_ids = fields.One2many("res.calcul.marge","Calculer_id")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='SOCIETE')
    currency_id = fields.Many2one(related="company_id.currency_id", string="Devise", readonly=True)

    @api.one
    @api.depends('margetotal_ids','margetotal_ids.prixacha','margetotal_ids.prixven')
    def _calcumargtotal(self):
        currentmar=0
        for mar in self.margetotal_ids:
            currentmar = currentmar + mar.prixven/mar.prixacha
        self.margtotal = currentmar

    margtotal = fields.Float(string="Marge Totale", store=True, compute="_calcumargtotal")

class Entreprise_account_analytic_line(models.Model):
    _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'
    
    person_id = fields.Many2one("res.partner","Reference")
    indemni = fields.Monetary(string="(4) Indemnites de nourriture et d'entretien", currency_fields="company_currency_id", store=True)
    acomp = fields.Monetary(string="(5) Acomptes verses dans le mois ", currency_fields="company_currency_id", store=True)

class Entreprise_res_company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    personne = fields.Many2one("res_gestpitem","company_id")

class Entreprise_res_gestp(models.Model):
    _name = 'res.gestp'
    item_id = fields.Many2one("account.analytic.line","Reference")
    debut_date = fields.Float(string="Date de debut du projet",related='item_id.date', store=True, readonly=True)
    fin_date = fields.Date("Date des conges du mois")
    debut_date = fields.Date(string='Date de debut du projet', related='item_id.date', store=True, readonly=True)
    nbre_jour = fields.Float(string='Nombre de jour', related='item_id.unit_amount', store=True, readonly=True)
    period = fields.Float("Nombre de jour du mois")
    Calcul_id = fields.Many2one("res.personnes","Reference partenaire")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='SOCIETE')
    currency_id = fields.Many2one(related="company_id.currency_id", string="Devise", readonly=True)
    
class Entreprise_res_gestpitem(models.Model):
    _name = 'res.gestpitem'
    adress = fields.Char("Adresse")
    banq = fields.Many2one("res.bank","Banque")
    name = fields.Many2one("res.personnes","Nom")
    item_ids = fields.One2many("account.analytic.line","person_id")
    item_id = fields.Many2one("account.analytic.line","Reference")
    nbre_jour = fields.Float(string="Nombre d'heures de travail", related="item_id.unit_amount", store=True, readonly=True)
    numero_CNPS = fields.Char("Numero d'immatriculation a la CNPS")
    numero_securite_sociale = fields.Char("Numero de securite sociale")
    periode = fields.Date("Periode")
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='SOCIETE')
    currency_id = fields.Many2one(related="company_id.currency_id", string="Devise", readonly=True)
    item_ids1 = fields.One2many("res.gestp","Calcul_id")
    
    @api.one
    @api.depends('item_ids1','item_ids1.nbre_jour','item_ids1.period')
    def _caljr(self):
        currentjr=0
        for jr in self.item_ids1:
            currentjr = currentjr + jr.nbre_jour * jr.period
        self.totaljr = currentjr

    totaljr = fields.Float(string="Nombre d'heures de gardes reelles", store=True, compute="_caljr")
    
    @api.one
    @api.depends('item_ids','item_ids.unit_amount','item_ids.amount')
    def _cal(self):
        currentci=0
        for ci in self.item_ids:
            currentci = currentci + ci.unit_amount * ci.amount * 1/240
        self.totalci = currentci

    totalci = fields.Monetary(string="Salaire Net", currency_fields='company_currency_id', store=True, compute="_cal")

    @api.one
    @api.depends('item_ids','item_ids.unit_amount','item_ids.amount')
    def _calim(self):
        currentim=0
        for im in self.item_ids:
            currentim = currentim + im.unit_amount * im.amount * 348/2400000 
        self.totalim = currentim

    totalim = fields.Monetary(string="(3.1) IGR+CN+IS impossable", currency_fields='company_currency_id', store=True, compute="_calim")

    @api.one
    @api.depends('item_ids','item_ids.unit_amount','item_ids.amount')
    def _calnon(self):
        currentnon=0
        for non in self.item_ids:
            currentnon = currentnon + non.unit_amount * non.amount * 614/2400000 
        self.totalnon = currentnon

    totalnon = fields.Monetary(string="(3.2) CRN non impossable", currency_fields='company_currency_id', store=True, compute="_calnon")
   
    @api.one
    @api.depends('item_ids','item_ids.unit_amount','item_ids.amount')
    def _calsoc(self):
        currentsoc=0
        for soc in self.item_ids:
            currentsoc = currentsoc + soc.unit_amount * soc.amount * 937/2400000 
        self.totalsoc = currentsoc

    totalsoc = fields.Monetary(string="(3.3) Securite sociale", currency_fields='company_currency_id', store=True, compute="_calsoc")
    
    @api.one
    @api.depends('item_ids','item_ids.unit_amount','item_ids.amount')
    def _calret(self):
        currentret=0
        for ret in self.item_ids:
            currentret = currentret + ret.unit_amount * ret.amount * 761/2400000 
        self.totalret = currentret

    totalret = fields.Monetary(string="(3.4) Assurance chomage et retraite complementaire IRCEM", currency_fields='company_currency_id', store=True, compute="_calret")

    @api.one
    @api.depends('item_ids','item_ids.unit_amount','item_ids.amount')
    def _calcot(self):
        currentcot=0
        for cot in self.item_ids:
            currentcot = currentcot + cot.unit_amount * cot.amount * 348/2400000 + cot.unit_amount * cot.amount * 614/2400000 + cot.unit_amount * cot.amount * 937/2400000 + cot.unit_amount * cot.amount * 761/2400000
        self.totalcot = currentcot

    totalcot = fields.Monetary(string="TOTAL DES COTISATIONS SOCIALES", currency_fields='company_currency_id', store=True, compute="_calcot")

    @api.one
    @api.depends('item_ids','item_ids.unit_amount','item_ids.amount','item_ids.indemni','item_ids.acomp')
    def _calmon(self):
        currentmon=0
        for mon in self.item_ids:
            currentmon = currentmon + mon.indemni + mon.unit_amount * mon.amount * 1/240 + mon.acomp * -1 
        self.totalmon = currentmon

    totalmon = fields.Monetary(string="MONTANT NET A PAYER", currency_fields='company_currency_id', store=True, compute="_calmon")
