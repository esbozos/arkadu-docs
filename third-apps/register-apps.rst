.. highlight:: rst
.. Registrar Apps de terceros:

La plataforma cuenta con un avanzado API que permite desarrollar Aplicaciones
que extiendan las funciones o interactuen con la plataforma.

Para ello el administrador con privilegios de super usuario debe crear las credenciales de
las Aplicaciones.

==================================
Registrar Aplicaciones de Terceros
==================================
Existen varias formas para registrar una nueva aplicación, la primera de ellas es a través del panel administrativo de django. Allí encontraremos **Oauth Provider** y a continuación seguiremos el vínculo de agregar nueva aplicación. 

En el formulario de creación, tendremos los siguientes parámetros que serán similares en cada una de las opciones de creación de aplicaciones. 

## campos del formulario

* Nombre: será la identificación en formato de texto que nos ayudará a distinguir la aplicación en el sistema y poder generar o revocar los token de autorización. 
* client_id: Hash string, generado automáticamente por el sistema, sin embargo puede editarlo y ajustarlo según corresponda. Si está migrando una app de una versión antigua del sistema, o simplemente desea proporcionar integración con otras credenciales *oauth*, puede pegar dichos valores en el formulario; también es posible editarlo posteriormente. 
* client_secret: Hash String, generado automáticamente por el sistema. Aplican las mismas condiciones que para el client_id.
* Client_type:
* Grant_type: client type password
* confidencial: public or private 
* return path:


======================
Agentes de recaudación
======================

En Arkadu trabajamos con el objetivo que el proceso de pago y recaudación sea lo más ágil y efectivo posible. 
Para ello creamos una interfaz de comunicación robusta, 100% segura y fácil para implementar con sistemas de pago de terceros.

# Activar un agente recaudador 
Es muy sencillo, tan sólo se requieren 3 pasos:
* Registrar una app de terceros y registrar el callback para notificar resultados de operaciones.
* Identificar al usuario responsable de las operaciones de recaudación (debe ser un usuario/email registrado en el sistema) y otorgar el ROL de 'Agente de recaudación'
* Generar el token Oauth y extender su validez por un tiempo superior al predeterminado (90 días en la configuración por defecto)


## Consultas al sistema 

El agente recaudador va a tener permisos para realizar solicitudes con los métodos GET, POST y UPDATE. Para ello se realiza un flujo básico de solicitudes que permiten garantizar la transacción de forma asíncrona.

Importante, cada solicitud debe incluir el Header Authorization de la siguiente manera:

('Authorization', 'Bearer <Token>')

Utilizando el token otorgado por la institución.  De lo contrario se generarán todas las solicitudes. 

### Consultar Cuentas por pagar 

Todos los agentes de recaudación pueden consultar las cuentas por pagar de un contribuyente, incluso si se trata de adquisición de artículos creados en la tienda virtual. 

* Method: GET
* Path: {Host_SERVER}/api/payments/pending/
* body: doc_id _String CI o RIF_

En el repsonse recibirá en formato JSON, conteniendo un array de objetos con los conceptos pendientes por pagar, el sistema realiza una consulta transversal a través de todos los módulos y refiere un id único para cada uno de ellos. 
 
#### Respuesta positiva 
Obtendrá siempre un True | 1 en el parámetro "res" 
'''
{"res": 1, data: {
 [{Id: Integer, amount: Decimal, description: String}]
}}
'''
#### Respuesta negativa 
Obtendrá un valor False | 0 acompañado del código de error y mensaje descriptivo
'''
{"res": 0, error: VARCHAR, message: String }
'''

*cada consulta queda registrada en los logs del sistema y puede ser auditada. Así mismo se pueden establecer alarmas de seguridad para usuarios de recaudación con actividad inusual en el sistema, para ello debe comunicarse con nuestro equipo de soporte.*


### Crear orden de pago 

Luego de haber recibido el array de cuentas por pagar el agente de recaudación debe seleccionar los conceptos a incluir en la orden de pago en una solicitud de la siguiente manera:

- Method: POST
- Path: {Host_SERVER}/api/payments/pending/
- Body: pending_ids: Array [Integer]

Incluyendo todos los IDs identificados a través de la primera solicitud GET vayan a ser incluidos en la orden de pago. 

Obtendrá un Response con los siguientes parámetros:

#### Orden de pago creada exitosamente 

'''
{"res": 1, order: Integer ID, total_amount: Decimal, expire_at: DateTime,  detail: {
 [{Id: Integer, amount: Decimal, description: String}]
}}
'''

Es importante identificar el tiempo de vencimiento de la orden de pago. Por defecto el sistema establece un lapso de 4 horas para reportar la recaudación. Durante este tiempo el usuario no podrá cambiar de agente de recaudación sobre los items elegidos para el pago. 

#### Error Al Crear la orden de pago 
'''
{"res": 0, error: VARCHAR, message: String }
'''

#### Agregar o eliminar items de la orden de pago 

- Method: UPDATE
- Path: {Host_SERVER}/api/payments/pending/
- Body: pending_ids: Array [Integer], order_id: UUID, action: ADD | REMOVE 

#### Orden de pago actualizada exitosamente 

'''
{"res": 1, order: Integer ID, total_amount: Decimal, expire_at: DateTime,  detail: {
 [{Id: Integer, amount: Decimal, description: String}]
}}
'''

### Reportar pago recibido 


- Method: POST
- Path: {Host_SERVER}/api/payments/pending/
- Body: order_id: UUID, amount: Decimal,   Reference: VARCHAR, created : DateTime, result :  Approved

### Anular orden de pago 

- Method: POST
- Path: {Host_SERVER}/api/payments/pending/
- Body: order_id: UUID, action: Cancel

### Resultados de orden de pago 

El sistema trabaja de forma asíncrona con la capacidad de recibir múltiples operaciones de recaudación sin detener la cola de procesamiento a la espera que cada operación realicé toda los procesos de dispatch, signals y listeners requeridos para operar sobre todos los módulos. 

Por ello al recibir un reporte de pago recibido, el agente recaudador obtendrá un Response básico de status OK. 

Sin embargo, recibirá un callback a través de la URL asignada en su aplicación registrado con las actualizaciones del procesamiento de cada item incluido en la orden de pago. Para ello debe disponer de un certificado SSL y tener disponible el puerto 443 a través del cual el sistema le hará reportes en método POST con la siguiente estructura.

- body: order_id, Reference, item_id, status: Success | Error, created, order_status: Processing | Complete | Canceled 

De esta forma se pueden anular pagos de forma asíncrona durante los procesos de consolidación y/o auditoría.

Así mismo, el sistema notificará al usuario del estado de cada uno de los items incluidos en su orden de pago a través de SMS, notificaciones PUSH y/o SMS. 







