# HCM-Prueba
Prueba de ingreso para HCMFront, según la siguiente [Guía](https://github.com/pdonaire1/HCM-Prueba/blob/master/Vacante%20Desarrollador%20HCMFront.pdf)
# Fase I
Solicitud de vacante (La base de datos sqlite ya posee data). 

Como objetivo de esta prueba se busca desarrollar (estructurar, diseñar y implementar) un
módulo que permita enviar solicitudes de vacante con una serie de aprobaciones para la posterior
asignación y creación de un proceso. [leer más...](https://github.com/pdonaire1/HCM-Prueba/blob/master/Vacante%20Desarrollador%20HCMFront.pdf)

**Instalación:**
```
pip install requirements.txt
python manage.py runserver
```
**Contraseña:** `usuario123`

**Usuarios:**

* admin
* solicitante
* aprobador1
* aprobador2
* jefe_directo
* responsable
* solicitante

**Para agregar un usuario**, despues de crear el objeto `User` es necesario, después de haberlo creado Agregar un objeto del tipo `Usuario` y asignar su respectivo rol, puede ser desde el admin.

# Fase II 
* [Pregunta 1](https://github.com/pdonaire1/HCM-Prueba/blob/master/fase_ii_pregunta_i.py)
Crear un método que reciba un string y quite los caracteres duplicados consecutivos, tener
en cuenta que el string contiene solo letras latinas minúsculas.
* [Pregunta 2](https://github.com/pdonaire1/HCM-Prueba/blob/master/fase_ii_pregunta_ii.py)
Un entero se considera redondo si termina con uno o más ceros. Dada una lista de enteros
encontrar el número redondo mas alto en ella y devolver su posición en la lista, si no hay
números redondos en la matriz devolver -1.
