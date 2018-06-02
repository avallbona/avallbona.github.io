Title: Lookup fields customitzats en Django
Date: 2018-06-03 10:41
Modified: 2018-06-03 10:41
Category: Django
Tags: django, queryset
Slug: django-lookup-fields
Authors: Andreu
Summary: Short version for index and feeds


Django, de manera genèrica, ens proveeix una API del seu ORM a través de la qual ens permet 
executar els "<a href="https://docs.djangoproject.com/en/1.9/ref/models/querysets/">querysets</a>" 
que necessitem de manera més o menys optima. Malgrat això, es pot donar el cas que necessitem 
realitzar algun tipus de consulta una mica més customitzada o millorada. Per a tal efecte, 
disposem de tota una sèrie d'eines, ja siguin els 
<a href="https://docs.djangoproject.com/en/1.9/ref/models/querysets/#q-objects">objectes Q</a>, 
les <a href="https://docs.djangoproject.com/en/1.7/ref/models/queries/#django.db.models.F">expressions F</a>, 
els <a href="https://docs.djangoproject.com/en/1.9/topics/db/queries/#field-lookups">Field Lookups</a>, etc. 
Sobre aquest darrer grup, els <strong>Field lookup</strong>'s tenim la possibilitat de definir 
els nostres propis.

Per a implementar un "Lookup field" hem d'implementar una classe que ens permeti personalitzar 
la part esquerra i la part dreta de la clàusula sql. Es fa estenent la classe <code>Lookup</code> 
del paquet "<code>django.db.models.fields.Lookup</code>" i, posteriorment, registrant aquest classe 
personalitzada amb el mètode <code>register_lookup</code> de la classe <code>django.db.models.fields.Field</code>. 
E.g.:


```python
from django.db.models import Lookup
from django.db.models.fields import Field


class Lower(Lookup):
    """
    Custom lookup for postgres "lower" function implementation
    """

    lookup_name = 'lower'

    def as_sql(self, qn, connection):

        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return 'lower({}) = {}'.format(lhs, rhs), params

Field.register_lookup(Lower)
```

L'exemple en concret implementa la funcionalitat de comparar el contingut d'un camp en 
minúscula amb la cadena que nosaltres li passem. Hi ha varis punts importants:

<code>lookup_name = 'lower'</code>
Defineix el nom que emprarem per executar la clàusula.

<code>lhs, lhs_params = self.process_lhs(qn, connection)</code>
Compila la part esquerra de la clàusula

<code>rhs, rhs_params = self.process_rhs(qn, connection)</code>
Compila la part dreta de la clàusula

<code>Field.register_lookup(Lower)</code>
Registrem el custom lookup per tal de poder-lo emprar.

Finalment, un exemple d'ús del nostre custom lookup seria:


```python
try:
    task = TransTask.objects.filter(object_class__lower=class_name).get()
except TransTask.DoesNotExist:
    task = None
```

<code>object_class__lower=class_name</code>
és la part on s'aplica el "custom lookup". Compararà el contingut en minúscula del camp 
<code>object_class</code> amb el contingut de la variable <code>class_name</code>.