# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError, ValidationError


class sedes_uniacme(models.Model):
    _name = 'sedes.uniacme'
    _description = 'Sedes de la Universidad Uniacme'
    
    name = fields.Char(string='Nombre de la Sede', required=True)
    
    






class estudiantes_candidatos(models.Model):
    #_name = 'candidatos.uniacme'
    _inherit = 'res.partner'
    _description = 'Canditatos y Estudiantes de la universidad'
    
    #name = fields.Char('Nombre', required=True)
    tipo_persona = fields.Selection([('estudiante', 'Estudiante'), ('candidato', 'Candidato')],string='Tipo de Persona')
    nro_identificacion = fields.Char(string='Número de Identificación', required=True)
    carrera = fields.Char(string='Carrera')
    sede_universitaria = fields.Many2one('sedes.uniacme', string='Sede Universitaria')
    procesos_votacion = fields.One2many('proceso.votaciones','candidatos', string='Procesos de Votacion')
    
    @api.constrains('nro_identificacion')
    def _unique_nro_identificacion(self):
        for record in self:
            res = self.search_count([("nro_identificacion", "=", record.nro_identificacion)])
            if  res > 1:
                raise ValidationError(f"Ya existe una persona con el numero de identificacion {record.nro_identificacion} .")