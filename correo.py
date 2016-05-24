#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Función que realiza el envío de correos con información obtenida de redes internacionales (NEIC, GEOFON)
v(1) 2016-05-21
autor: Daniel Siervo
e-mail: dsiervo@sgc.gov.co
"""
import smtplib 
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import system
from datetime import datetime, timedelta
import time

def correo(source,date,hour,lat,lon,dep,M,region,ID,mapa, link):
    
    #Formatea strings con hora local de evento y de boletin
    Date_b=datetime.now()
    delta = timedelta(hours=5)
    format =  "%Y-%m-%d %H:%M:%S"
    strd = str(Date_b - delta)
    local = datetime.strptime(date+' '+hour, format)
    localtime = str(local - delta)

    #lee datos del remitente
    datosr=open('remitente.txt','r').readlines()
    
    #Prepara correos electrónicos con información del sismo.boletin
    print 'Preparando correo...'
    remitente = datosr[0] 
    passw= datosr[1]
    destinatario = "hchamorro@sgc.gov.co, l_analistas-rsnc@sgc.gov.co, l_sismologia-rsnc@sgc.gov.co, rsncol@sgc.gov.co"# nperez@sgc.gov.co"
    asunto = "ESTO ES UNA PRUEBA!!!Sismo internacional reportado como sentido en Colombia, %s"%(region) 
    mensaje1=open('sismo.boletin').read()%(strd,localtime.split(' ')[0],localtime.split(' ')[1],date,hour,M,region,lat,lon,dep,M,source,link)
    
    #Prepara asunto y remitentes
    msg = MIMEMultipart()
    msg['Subject'] = asunto
    msg['From'] = datosr[0]
    
    #Prepara destinatarios y adjunta imagen
    msg['To'] = destinatario
    fp=open(mapa, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    text = MIMEText(mensaje1)
    print mensaje1
    msg.attach(text)    
    
    #inicia servicio de envío de correos
    server = smtplib.SMTP('smtp.gmail.com:587') 
    server.starttls()
    server.login(remitente,passw)
    
    region = '_'.join(region.split())
    #Pregunta si se desea enviar correos
    u=raw_input('Para enviar el correo e insertar la informacin a la base de datos digite 1, de lo contrario enter: \n')
    #Envía correos
    if u=='1':
        server.sendmail(remitente, destinatario.split(", "), msg.as_string())
	#print type(source),type(date),type(hour),type(lat),type(lon),type(dep),type(M),type(region)
        system('sh conexion.sh %s %s %s %s %s %s %s %s %s %s %s'%(ID,source,date,hour,lat,lon,dep,M,region,localtime.split()[0], localtime.split()[1]))
	#system('sh /mnt/internacionales/pruebas/sismosinternacionales/internacionales-yo.sh %s %s %s %s %s %s %s' %(lat,lon,dep,M,'prueba',date,hour))
	print 'envio parametros'
    else: print 'No se enviÃ³ correo'
    
    server.quit()
