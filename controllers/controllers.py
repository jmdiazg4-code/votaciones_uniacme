# -*- coding: utf-8 -*-
from odoo import http


class VotacionesUniacme(http.Controller):

    @http.route('/funcion_button', methods=['GET'], type='http', auth='user', website=True)
    def refrescar_website(self):
        print('presiono actualizar')
        clase = http.request.env['ir.module.module'].search([('name', '=', 'votaciones_uniacme')])
        # print('entro al funcion ACTUALIZAR CONTACTOS')
        clase.button_immediate_upgrade()

        return http.request.redirect('/ingreso')
    
    
    

    #Validacion de cedula
    @http.route('/get_identificacion', methods=['POST','GET'], type='http', auth='public', website=True)
    def ingreso(self, **kw):
        nro_id = kw.get('nro_identificacion')
        if nro_id:
            estudiante = http.request.env['res.partner'].sudo().search([('tipo_persona','=','estudiante'),('nro_identificacion', '=', nro_id)])
            procesos_votacion = http.request.env['proceso.votaciones'].sudo().search([('estado_related','=','proceso')])
            print('procesos ',procesos_votacion)
            if estudiante:
                return http.request.render('votaciones_uniacme.page_proceso_votacion', {'estudiante': estudiante, 'procesos':procesos_votacion})
            else:
                print('No existe')
                return http.request.render('votaciones_uniacme.ingreso_denegado',{})
                
                
        saludo = 'Hola desde el controller'
        #return http.request.render('votaciones_uniacme.page_ingreso', { 'estudiante':estudiante})


    # Selecciona el proceso de votacion
    @http.route('/proceso_votacion', methods=['POST','GET'], type='http', auth='public', website=True)
    def select_proceso_votacion(self, **kw):
        estudiante = kw.get('estudiante')
        proceso_votacion = kw.get('proceso_votacion')
        voto = http.request.env['votacion.online'].sudo().search([('proceso_votacion', '=', int(proceso_votacion)),('sufragante','=',int(estudiante))])
        print('result  ', voto)
        if voto:
            print('Ya votó')
            return http.request.render('votaciones_uniacme.voto_duplicado',{})
        else:
            print('no voto')
            candidatos_ids = http.request.env['proceso.votaciones'].sudo().search([('id', '=', int(proceso_votacion))]).candidatos
            return http.request.render('votaciones_uniacme.page_eleccion_candidato',
                                       {'estudiante': estudiante, 'proceso': proceso_votacion, 'candidatos': candidatos_ids})

    # Selecciona el proceso de votacion
    @http.route('/select_candidato', methods=['POST', 'GET'], type='http', auth='public', website=True)
    def select_candidato(self, **kw):
        estudiante = int(kw.get('estudiante'))
        proceso_votacion = int(kw.get('proceso'))
        candidato = int(kw.get('candidato'))
        voto = http.request.env['votacion.online'].sudo().create({
            'proceso_votacion': proceso_votacion,
            'sufragante': estudiante,
            'candidato_id': candidato
        })
        print('creado ', voto)
        if voto:
            return http.request.render('votaciones_uniacme.votacion_final',{'voto': voto})
        else:
            return http.request.render('votaciones_uniacme.votacion_final', {'voto': voto})

    @http.route('/finalizar_votacion', methods=['GET'], type='http', auth='public', website=True)
    def finalizar_votacion(self):
        return http.request.redirect('/ingreso')