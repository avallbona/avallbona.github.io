Title: Formateig per defecte de les dates amb Django
Date: 2015-09-13 21:32
Author: blogadmin
Category: Django, Feina
Tags: date format, django, strftime
Slug: formateig-per-defecte-de-les-dates-amb-django
Status: published

Al principi de començar amb **Django** me vaig trobar amb el problema
del format de les dates. Per a la part de frontend no és massa
problemàtic ja que podem fixar noltros el format de cada data en
particular. Per exemple:  

    {% trans 'Fecha salida' %}: {{ reservation.departure_date_res|date:'d/m/Y' }}  
  
El problema sorgeix amb, per exemple, el format de les dates de
l'administrador, el qual està determinat pels valors per defecte de
django.

Aquests solen variar en funció de l'idioma de l'usuari i/o del
navegador. Per corregir aquests fet, **Django** ens proporciona un
mètode per poder fixar els formats per defecte de les dates. Al
directori on està definit el projecte s'ha de creat una carpeta
"formats" que contingui un directori per a cada idioma (es, ca, de, en, ...) i que, cadascuna d'aquestes contingui un arxiu "formats.py" amb els
formats de les dates. 

Llavors al settings.py s'ha d'afegir una linia per indicar d'on s'ha
d'agafar el format de les dates:
  
    FORMAT_MODULE_PATH = 'balearictransfer.formats'  

També es poden indicar el format de les dates pels "inputs" de les
dates, així com el separador decimal o de mils, per exemple:
  
    DATE_INPUT_FORMATS = (  
        '%d-%m-%Y', # '21-03-2014'  
    )  
    TIME_INPUT_FORMATS = (  
        '%H:%M:%S', # '17:59:59'  
        '%H:%M', # '17:59'  
    )  
    DATETIME_INPUT_FORMATS = (  
        '%d-%m-%Y %H:%M', # '21-03-2014 17:59'  
    )

    DECIMAL_SEPARATOR = u'.'  
    THOUSAND_SEPARATOR = u','  
    NUMBER_GROUPING = 3  

A **Github** podeu trobar un [projecte de mostra](https://github.com/andilabs/demo_time_set) que explica com
funciona el tema. I també la [pertinent explicació](http://stackoverflow.com/a/22565251) a **Stack Overflow**
