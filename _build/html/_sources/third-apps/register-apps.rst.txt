.. highlight:: rst
.. Registrar Apps de terceros:

La plataforma cuenta con un avanzado API que permite desarrollar Aplicaciones
que extiendan las funciones o interactúen con la plataforma.

Para ello el administrador con privilegios de super usuario debe crear las credenciales de
las Aplicaciones.


    **TEMPORALMENTE EL API ESTARÁ SIRVIENDO EN LA URL https://old.arkadu.com**

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

Activar un agente recaudador
____________________________

Es muy sencillo, tan solo se requieren 3 pasos:

- Registrar una app de terceros.
- Identificar al usuario responsable de las operaciones de recaudación (debe ser un usuario/email registrado en el sistema) y otorgar el ROL de **"Agente de recaudación"**
- Generar el token Oauth y extender su validez por un tiempo superior al predeterminado (90 días en la configuración por defecto)


Integración con el API de recaudo
_________________________________

Para poder realizar las operaciones descritas a continuación, su aliado comercial debe proporcionarle los siguientes datos:

- client_id
- client_secret
- access_token
- refresh_token
- customer_id (opcional si solo hará recaudo para una cuenta en **Arkadu**)

    **NOTA** *Todos estos datos son confidenciales y deben ser almacenados en un lugar seguro.* 
    *En caso de presentar algún incidente de seguridad, por favor reportarlo para revocarlos y solicitar la generación de nuevas credenciales.*

Consultas al sistema 
====================

Todas las peticiones al API deben cumplir con las siguientes condiciones:

:HOST arkadu.com:

    El host que responderá autoritativamente a las peticiónes del API siempre será arkadu.com

:Protocolo HTTPS:
    Todas las peticiones deben ser realizadas a través del protocolo *HTTPS* cualquier petidición
    realizada en HTTP (puerto: 80) serán redirigidas automáticamente al puerto 463 implementando 
    el certificado SSL/TLS. Asegúrese que su cliente de peticiones sea compatible con la verficiación
    de las firmas. 
    Toda petición a través de HTTP que no acepte redireccionamiento, será rechazada.

:Método POST:
    El método de la petición siempre será *POST*, toda solictud que implemente otro método
    será rechazada como *Método no Válido*

:Encabezados Content-Type y Authorization:
    Todas las peticiones deben incluir los siguientes encabezados
        
.. code-block:: python
    :emphasize-lines: 3,5

    headers = { 
        "Content-Type": "application/json",
        "Authorization": "Bearer <access_token>"
    }
    
*Excepto las peticiones no autenticadas, como la renovación del token.*

:Cuerpo JSON:
    El cuerpo de las peticiones deben ser en formato JSON.

Consultar Ordenes de Pago y/o productos
=======================================

    El principal rol del agente de recaudo es recibir los pagos de usuarios a 
    nombre de un cliente activo en Arkadu. Para ello se inicia con una consulta
    de las ordenes de pago abiertas creadas por el usuario, o los productos pendientes
    de pago en el sistema.

.. image:: /third-apps/consulta_ejemplo_input.png
    :height: 400

.. literalinclude:: /third-apps/arkadu_get_orders.py
    :language: python
    

Elementos importantes:
######################

country: 
    Al realizar una consulta de ordenes de usuario, debemos identificar
    el código ISO 3166-1 alpha-2 del país del documento de identidad 
    
doc_id:
    Documento de identidad formateado según la estructura del país. 

Estructura de las respuestas
____________________________

Todas las respuestas al API responderán con data en formato JSON, el
resultado del ejemplo anterior sería algo así:

.. literalinclude:: /third-apps/result_get_orders.json
    :language: json

-----

.. image:: /third-apps/resultados_ejemplo.png
    :height: 400

Respuesta Existosa
##################

Toda respuesta exitosa al API está estructurada de la siguientes manera

- res = 1
- data = JSON data
- status = 200

En el ejemplo anterior, el sistema del agente recaudador deberá mostrarle 
al usuario final (Operador de caja, HomeBanking, App Móvil, entre otros),
un menú de elección simple para el caso de las ordenes y múltiple para el
caso de los productos.


Respuesta No Existosa
#####################       


Toda respuesta rechazada al API tendrá la siguiente estructura

- res = 0
- messages = "cadena de texto"
- code = "Código Interno del API para identificar el error"
- status = HTTP STATUS CODE 400+


Elegir Items a pagar
____________________

En el ejemplo de consulta anterior. Recibimos una respuesta que contiene
una order identificada con el *ID 2052042* y una serie de productos que 
le pertenecen directamente al usuario consultado.

Elementos importantes
######################

orders:
    - id -> *2051963*
    - owner -> será nuestro user_id = *109679*
    - customer -> id *10050482* Nos permite presentarle información personalizada al usuario sobre a quien va dirigido el pago.
    - get_total -> será nuestro monto a pagar para la orden.

Luego de haber recaudado el importe de la orden, procedemos a reportar el pago de la misma al API de arkadu.

.. registrar_pago:

Registrar Pago
_______________

Para ello debemos indicar los datos obtenidos previamente en la consulta.

.. literalinclude:: /third-apps/arkadu_register_payment.py
    :language: python

Del proceso de registro de pago recibiremos una respuesta del API con los datos
del pago:

.. literalinclude:: /third-apps/respuesta_de_pago.json
    :language: json

Elementos Importantes
_____________________

- id : Id del pago en Arkadu. deberá relacionarse internamente para cualquier reverso u operación de reclamos.
- state: 'approved' este estado nos indica que ha sido exitoso el proceso de pago de la orden.
- reference: debe coincidir con la proporcionada por el agente de recaudo al momento de registrar el pago.
- owner: contiene los datos del usuario pagador. sirve de validación y para emisión de recibos y/o facturas.
- admin: coincide con el usuario que ha registrado el pago / agente de recaudo.
- amount: El monto registrado de pago por la orden.

En caso que realice más de una solicitud con los mismos datos, la segunda respuesta indicará que ya existe un pago
registrado para esa orden, el res=0, pero tendremos los detalles del pago para validar si la referencia y el admin
ha sido el del agente recaudador. 

.. literalinclude:: /third-apps/ejemplo_pago_duplicado.json
    :language: json


Reporte de Movimientos
_______________________

Si el agente recaudador es el administrador de cuenta (Banco, plataforma de pagos dígitales, Caja de efectivo)
una de las principales atribuciones es el reportar los movimientos y balance de cuenta de forma recurrente al cliente en Arkadu
esto permite mantenerle informado sobre el proceso de recaudo, informar operaciones de debito y credito adicionales, asi como las comisiones causadas
por el servicio de recaudación.

Para ello se recomienda el uso de cronjobs al menos una vez al día, con el reporte de cuenta.

.. literalinclude:: /third-apps/arkadu_reporte_de_movimientos.py
    :language: python


Una vez más obtenemos una respuesta del API con la siguiente estrcutura.

.. literalinclude:: /third-apps/respuesta_movimientos.json
    :language: json


Crear Orden con productos
____________________________

Como vimos en Consultar Ordenes de Pago y/o productos el sistema además de las ordenes pendientes de pago
también nos envía los productos individuales que no han sido pagados por el usuario o productos disponibles en la
tienda del cliente para pagos estandar.

Esta opción es exclusiva de la selección de la orden; Es decir, si se elige una orden a pagar no se debe permitir
elegir productos individualers y viceversa.


.. literalinclude:: /third-apps/arkadu_create_order.py
    :language: python


Nuevamente el API nos reponde con los datos de la orden recien creada, el cual podemos proceder
a recaudar inmediatamente. Es decir no require el proceso de selección de orden.

.. literalinclude:: /third-apps/ejemplo_respuesta_crear_orden.json
    :language: json


Tomamos el ID de la nueva orden (2051912 en el ejemplo) y realizamos la misma operación de 
registro de pago indicado en la sección de arriba :ref:`Registrar Pago`.

Renovar Access Token
====================

Por seguridad es recomendable renovar el access_token frecuentemente. para ello
debemos hacer un request al API de la siguiente manera:

.. literalinclude:: /third-apps/arkadu_renovar_token.py
    :language: python

