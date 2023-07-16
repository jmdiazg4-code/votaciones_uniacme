from odoo import fields, models, api, exceptions
from xlrd import open_workbook,  xldate_as_datetime
from datetime import datetime

import base64

class ImportProcesoVotacion(models.TransientModel):
    _name = 'import.proceso.votacion'
    _description = 'Importación de Procesos de Votación'

    
    def _get_template(self):
        self.template = base64.b64encode(open("./../data/importvotaciones.xlsx", "rb").read())

    document = fields.Binary(string='Documento')
    template = fields.Binary('Template', compute="_get_template")
    
    
    def button_descargar(self):
        print('descargando')

        return {
            'type': 'ir.actions.act_url',
            'name': 'template',
            'url': '/web/content/import.proceso.votacion/%s/template/importvotaciones.xlsx?download=true' % (self.id),
        }


    
    def button_import(self):
       
        file_data = base64.b64decode(self.document)

        wb = open_workbook(file_contents=file_data)

        sheet = wb.sheet_by_index(0)

        values = sheet._cell_values
        print('Valores excel')
        print(values)
        tam = len(values)
        print('largo del array ', tam)
        format = '%d/%m/%YT%H:%M:%S+%f'
        


        encabezados= values[0]
        values.pop(0)
        print('encabezados ', encabezados)
        for record in values:
            print('Reggistro-- ', record)
            create = self.env.cr.execute(f"""INSERT INTO proceso_votaciones(
                                name, estado, fecha_inicio, fecha_fin)
                                VALUES (%(name)s,'borrador',%(fecha_inicio)s,%(fecha_fin)s);
                            """, {  "name": record[0],
                                    "fecha_inicio": xldate_as_datetime(record[1], 0),
                                    "fecha_fin": xldate_as_datetime(record[2], 0)
                                    })
            
        fecha_inicio_str = 45121.0
        fecha_fin_str = 5122.0
        fecha_inicio_object = datetime.fromtimestamp(fecha_inicio_str)
        fecha_fin_object = datetime.fromtimestamp(fecha_fin_str)
        print('Fecha - ', xldate_as_datetime(fecha_inicio_str,0), ' cadena ', fecha_fin_object.strftime(format))

      
        action = self.env['ir.actions.act_window']._for_xml_id('votaciones_uniacme.proceso_votaciones_act_window')
        return action
    
    
    