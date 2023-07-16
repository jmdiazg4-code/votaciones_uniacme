# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime

from odoo.exceptions import UserError, AccessError, ValidationError

class ProcesoVotaciones(models.Model):
    _name = 'proceso.votaciones'
    _description = 'Procesos de Votación'

    name = fields.Char(string='Descripción de la Votacion', required=True)
    fecha_inicio = fields.Datetime(string='Fecha de Inicio') 
    fecha_fin= fields.Datetime(string='Fecha de Finalización')
    estado = fields.Selection([('borrador','Borrador'),('proceso','En Proceso'),('cerrada','Cerrada')], default='borrador', string='Estado')
    estado_related = fields.Selection(related='estado', store=True)
    candidatos = fields.Many2many('res.partner', 
                                  'res_partner_candidato_rel', 
                                  'candidato_id', 
                                  'res_partner_candidato', 
                                  string='Candidatos',
                                  domain="[('tipo_persona', '=', 'candidato')]",)
    
    
    
    
    def button_proceso(self):
        for record in self:
            record.estado='proceso'
        
    def button_cerrar(self):
        for record in self:
            record.estado='cerrada'
                    
    @api.model           
    def verificar_vencimiento(self):
        records = self.env['proceso.votaciones'].sudo().search([('estado', '!=', 'cerrada')])
        for record in records:
            #print('entro desde la accion automatica')
            if record.fecha_fin:
                #print('fechas establecidas')
                #record.estado = 'proceso'
                if record.fecha_fin <= datetime.now():
                    #print('cerrando -..', record.name)
                    record.estado = 'cerrada'
            """else:
                print('asignando en borrador')
                record.estado = 'borrador'
            """
    
    def _inverse_estado(self):
        for record in self:
            if record.fecha_fin > datetime.now():
                record.estado = 'proceso'
            else:
                if record.fecha_inicio:
                    rec
    
    def action_btn_resultados_votacion(self):
        action = self.env['ir.actions.act_window']._for_xml_id('votaciones_uniacme.votacion_online_act_window')
        action['domain'] = [('proceso_votacion', '=', self.id)]
        return action
    
    
    def obtener_resultados_votacion(self, participantes, proceso):
        print('Proceso', proceso)
        resultados = []
        for rec in participantes:
            total_votos = self.env['votacion.online'].sudo().search_count([('proceso_votacion','=',proceso),('candidato_id','=',rec.id)])
            line = {
                'name': rec.name,
                'photo': rec.image_1920,
                'total': total_votos
            }
            resultados.append(line)
        print('total votos ', resultados)
        return resultados
        
    def action_imprimir_resultados(self):
        for record in self:
            participantes = record.candidatos
            print('participantes ', participantes)
            resultados = self.obtener_resultados_votacion(participantes,record.id)
            
        data = { 
            'resultados': resultados,
            'proceso': record.name
        }
        return self.env.ref('votaciones_uniacme.action_report_resultados_votacion').report_action([], data=data)
        
    
    
class VotacionesOnline(models.Model):
    _name = 'votacion.online'
    _description = 'Votación Online'
    
    
    
    
    proceso_votacion = fields.Many2one('proceso.votaciones', string='Proceso de Votación')
    candidatos_rel_ids = fields.Many2many(related='proceso_votacion.candidatos')
    sufragante = fields.Many2one('res.partner',  domain="[('tipo_persona', '=', 'estudiante')]" )
    candidato_id = fields.Many2one('res.partner', string='Candidato', domain="[('id','in',candidatos_rel_ids)]")
    
    
    
    def funcionp(self):
        print('entro a la funcion')
        return 'hola mundo'
    
    
   
    
    @api.depends('sufragante')
    def _get_sufragante(self):
        for record in self:
            default = self.env.user.partner_id
            print('sufra ', default)
            record.sufragante = default
    
    
    @api.constrains('proceso_votacion','sufragante')
    def _unique_voto_estudiante(self):
        for record in self:
            res = self.search_count([('proceso_votacion','=',record.proceso_votacion.id),('sufragante','=',record.sufragante.id)])
            print('cantidad ' , res)
            if  res > 1:
                raise ValidationError(f"Ya ha realizado su voto para  {record.proceso_votacion.name} el { record.create_date }.")

    