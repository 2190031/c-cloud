import paypalrestsdk
import arrow
import pytz
import datetime
import requests
import base64
import pycountry
import locale
from flask import jsonify, request, session, render_template, redirect
from babel.dates import format_date, format_time, format_datetime
from db_models import db, paytransaction, user, licence
from flask_mail import Message, Mail
from sqlalchemy.orm import Query
from sendMail import send_mail_fact


mail = Mail()

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "AdvcMAZRch_a2_IX8HcOahjLOrd0PGTh4sjj_Fq6UdgrVUsf38Gwttt04IVoCR5hc0nKcONkEGXjtghB",
    "client_secret": "EM2-afNHVKHKLSoFtoDKbQ4Ap1U3VTmaXiXT3-8CwOILetphM5qt_KwEy8244739kZSDGJddmbcGZ5ar"
})


def obtener_token_acceso_paypal():
    # URL del endpoint de autenticación de PayPal
    url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
    # Parámetros de la solicitud de autenticación
    data = {
        'grant_type': 'client_credentials'
    }
    # Encabezados de la solicitud de autenticación
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # Codifica las credenciales de cliente en base64
    auth_header = "Basic QWR2Y01BWlJjaF9hMl9JWDhIY09haGpMT3JkMFBHVGg0c2pqX0ZxNlVkZ3JWVXNmMzhHd3R0dDA0SVZvQ1I1aGMwbktjT05rRUdYanRnaEI6RU0yLWFmTkhWS0hLTFNvRnRvREtiUTRBcDFVM1ZUbWFYaVhUMy04Q3dPSUxldHBoTTVxdF9Ld0V5ODI0NDczOWtaU0RHSmRkbWJjR1o1YXI"

    # Agrega el encabezado de autorización al encabezado de la solicitud
    headers['Authorization'] = auth_header

    # Realiza la solicitud de autenticación a PayPal
    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        #print(f'COÑO AL FIN DIO MIO PADRE SANTO: {token_data} - {access_token}')
        return access_token
    else:
        #print(f'Error al obtener el token de acceso: {response.status_code} - {response.text}')
        #print(f'Error al obtener el token de acceso: {headers} - {response}')
        #print(response.text)
        return None

def enviar_factura(id_user, direccion_facturacion):
    # Realizar la consulta con INNER JOIN y obtener los campos necesarios
    transaction = db.session.query(paytransaction, user.username, licence.plan, user.email)\
    .join(user, paytransaction.iduser == user.iduser)\
    .join(licence, paytransaction.idlicence == licence.idlicence)\
    .filter(paytransaction.iduser == id_user)\
    .order_by(paytransaction.datepaid.desc())\
    .first()

    if transaction:
        # Obtener los valores de la transacción
        id_transaccion = transaction.paytransaction.paypal_transaction
        username = transaction[1]
        plan = transaction[2]
        email_destinatario = transaction[3]
        datepaid = transaction.paytransaction.datepaid
        total_amount = transaction.paytransaction.amount

        nombre_pais = obtener_nombre_pais(direccion_facturacion['country_code'])
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        locale.setlocale(locale.LC_TIME, 'es_ES')
        zona_horaria = session.get("zona_horaria");
        fecha_actual = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone(zona_horaria))
        fecha_formateada = format_datetime(fecha_actual, format='EEEE, d \'de\' MMMM \'de\' yyyy \'a las\' h:mm a', locale='es')
        # Crear un objeto de mensaje para el correo electrónico
        msg = render_template('factura.html', cliente=username, fecha=fecha_formateada, numero_factura=id_transaccion, nombre_plan=plan, total=total_amount, direc_cliente=direccion_facturacion, pais=nombre_pais)

        # Enviar el correo electrónico
        image_path = 'c-cloud/static/public/img/logo-lg.png'
        send_mail_fact(email_destinatario, 'C-Cloud Factura', msg, image_path=image_path)

    else:
        print('No se encontró ninguna transacción para el usuario')


def enviar_bienvenida(username, email, name):
        # Crear un objeto de mensaje para el correo electrónico
        msg = render_template('welcome.html', username=username, email=email, name=name)

        # Enviar el correo electrónico
        image_path = 'c-cloud/static/public/img/icon.png'
        send_mail_fact(email, 'Bienvenido/a a C-Cloud', msg, image_path=image_path)


def payment_basic():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "https://wady01.pythonanywhere.com/execute",
            "cancel_url": "https://wady01.pythonanywhere.com/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Plan Básico",
                    "sku": "BASICO",
                    "price": "9.99",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "9.99",
                "currency": "USD"
            },
            "description": "Plan básico de C-Cloud para el servicio"
        }]
    })

    if payment.create():
        print('Payment success!')
        return jsonify({'paymentID': payment.id})
    else:
        print(payment.error)
        return jsonify({'error': payment.error['message']})


def execute_basic():
    id_user = session.get('user_id')
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    access_token = obtener_token_acceso_paypal()  # Obtener el token de acceso

    if access_token:
        if payment.execute({'payer_id': request.form['payerID']}):
            print('Execute success!')
            success = True

            # Obtener los detalles de la transacción de PayPal
            amount = payment.transactions[0].amount.total
            zona_horaria = session.get("zona_horaria");
            fecha_actual = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone(zona_horaria))

            # Crear una instancia de PayTransaction y guardarla en la base de datos
            new_transaction = paytransaction(
                iduser=id_user,
                paypal_transaction=payment.id,
                idlicence=2,
                amount=float(amount),
                datepaid=fecha_actual
            )

            db.session.add(new_transaction)
            db.session.commit()

            # Obtener la dirección de facturación del cliente
            direccion_facturacion = obtener_direccion_comprador(payment.id,access_token)

            if direccion_facturacion:
                # Utiliza la dirección de facturación para tu lógica de envío de factura
                session["new_plan"] = "¡Compra realizada! En tu correo electrónico hemos enviado los detalles"
                enviar_factura(id_user, direccion_facturacion)
                return "Bien"
            else:
                session["new_plan"] = "¡Compra realizada! No se encontró la dirección de facturación del cliente"
                return "Bien"

        else:
            print(payment.error)
            return jsonify({'error': payment.error['message']})
    else:
        print('Error al obtener el token de acceso')
        return jsonify({'error': 'Error al obtener el token de acceso'})

def payment_premium():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "https://wady01.pythonanywhere.com/execute/premium",
            "cancel_url": "https://wady01.pythonanywhere.com/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Plan Premium",
                    "sku": "PREMIUM",
                    "price": "19.99",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "19.99",
                "currency": "USD"
            },
            "description": "Plan premium de C-Cloud para el servicio"
        }]
    })

    if payment.create():
        print('Payment success!')
        return jsonify({'paymentID': payment.id})
    else:
        print(payment.error)
        return jsonify({'error': payment.error['message']})


def execute_premium():
    id_user = session.get('user_id')
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    access_token = obtener_token_acceso_paypal()  # Obtener el token de acceso

    if access_token:
        if payment.execute({'payer_id': request.form['payerID']}):
            print('Execute success!')
            success = True

            # Obtener los detalles de la transacción de PayPal
            amount = payment.transactions[0].amount.total

            zona_horaria = session.get("zona_horaria");
            fecha_actual = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone(zona_horaria))
            # Crear una instancia de PayTransaction y guardarla en la base de datos
            new_transaction = paytransaction(
                iduser=id_user,
                paypal_transaction=payment.id,
                idlicence=1,
                amount=float(amount),
                datepaid=fecha_actual
            )

            db.session.add(new_transaction)
            db.session.commit()

            # Obtener la dirección de facturación del cliente
            direccion_facturacion = obtener_direccion_comprador(payment.id,access_token)

            if direccion_facturacion:
                # Utiliza la dirección de facturación para tu lógica de envío de factura
                enviar_factura(id_user, direccion_facturacion)
                session["new_plan"] = "¡Compra realizada! En tu correo electrónico hemos enviado la factura"
                return "Bien"
            else:
                session["new_plan"] = "¡Compra realizada! No se encontró la dirección de facturación del cliente"
                return "Bien"

        else:
            print(payment.error)
            return jsonify({'error': payment.error['message']})
    else:
        print('Error al obtener el token de acceso')
        return jsonify({'error': 'Error al obtener el token de acceso'})


def obtener_direccion_comprador(payment_id, access_token):
    # URL de la API de PayPal para obtener la información del pago
    url = f'https://api-m.sandbox.paypal.com/v1/payments/payment/{payment_id}'

    # Configura el encabezado de autenticación con el token de acceso
    headers = {'Authorization': f'Bearer {access_token}'}

    # Realiza la solicitud a la API de PayPal para obtener la información del pago
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        payment_data = response.json()
        direccion_comprador = payment_data['payer']['payer_info']['shipping_address']
        return direccion_comprador
    else:
        print(f'Error al obtener la información del pago: {response.status_code} - {response.text}')
        return None

def obtener_nombre_pais(codigo_pais):
    try:
        pais = pycountry.countries.get(alpha_2=codigo_pais)
        if pais is not None:
            return pais.name
    except pycountry.InvalidCountryException:
        pass

    return None




