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
##import time

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
    destinatario = "dsiervo@sgc.gov.co, ddsiervop@unal.edu.co"# nperez@sgc.gov.co"
    asunto = "ESTO ES UNA PRUEBA!!!Sismo internacional reportado como sentido en Colombia, %s"%(region) 
    mensaje1=open('sismo.boletin').read()%(strd[0:19],localtime.split(' ')[0],localtime.split(' ')[1],date,hour,M,region,lat,lon,dep,M,source,link)
    
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
    u=raw_input('Ingrese 1, 2, 3 o 4 deacuerdo a las siguientes opciones, enter para salir:\n\n \t1. Enviar boletín por correo \n \t2. Publicar \t \n\t3. Enviar correo y publicar \n\t4. Actualizar información en la página \n\n \t======: ')
    #Envía correos
    if u=='1':
        server.sendmail(remitente, destinatario.split(", "), msg.as_string())
        print 'Enviando correo...'
	
    elif u=='2':
        system('sh conexion.sh %s %s %s %s %s %s %s %s %s %s %s'%(ID,source,date,hour,lat,lon,dep,M,region,strd.split()[0], strd.split()[1]))
        print 'envió parametros a la base'
    elif u=='3':
        server.sendmail(remitente, destinatario.split(", "), msg.as_string())
        system('sh conexion.sh %s %s %s %s %s %s %s %s %s %s %s'%(ID,source,date,hour,lat,lon,dep,M,region,strd.split()[0], strd.split()[1]))
    elif u=='4':
        system('sh conexion.sh %s %s %s %s %s %s %s %s %s %s %s'%(ID,source,date,hour,lat,lon,dep,M,region,strd.split()[0], strd.split()[1]))
    else: print 'envió parametros a la base'
    
    server.quit()
