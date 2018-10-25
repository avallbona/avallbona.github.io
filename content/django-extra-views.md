Title: Django extra views
Date: 2015-09-12 20:56
Author: blogadmin
Category: Django, Feina
Tags: django extra viwws, django formset js, formset
Slug: django-extra-views
Status: published

"**[Django extra
views](https://github.com/AndrewIngram/django-extra-views)**" ens
proporciona una manera fàcil, a través de les seves vistes
"vitaminades", d'implementar els
"**[formsets](https://docs.djangoproject.com/en/1.8/topics/forms/formsets/)**"
per tal d'editar les relacions 1-n amb Django. Tambe tenir
**[django-formset-js](https://github.com/pretix/django-formset-js)** que
ens "dinamitza" a través de Javascript la inserció i eliminació de
tuples dels** "formsets"**.<!--more-->

Per instal.lar les "django extra views" cal executar:

    pip install django-extra-views  

Per instal.lar django-formset-js cal executar:  
    
    pip install django-formset-js  

i afegir l'aplicació al projecte:  
  
    INSTALLED\_APPS = (  
        ...  
        'djangoformsetjs',  
    )  

Detallant els passos, que serien:
  
**Views**:

# -*- encoding: utf-8 -*-

from crispy_forms.helper import FormHelper  
from crispy_forms.layout import Layout  
from crispy_forms.layout import Div

from django import forms

from extra_views import CreateWithInlinesView, UpdateWithInlinesView,
InlineFormSet  
from backoffice.cars.models import AssuranceFeaturePrice,
EquipmentPrice, ChargePrice  
from cms.cmscars.office.forms import AssuranceFeaturePriceForm,
EquipmentPriceForm, ChargePriceForm

#### views.py

```python
    class AssuranceFeaturePricesInline(InlineFormSet):  
        model = AssuranceFeaturePrice  
        form_class = AssuranceFeaturePriceForm  
        extra = 0
    
    class EquipmentPricesInline(InlineFormSet):  
        model = EquipmentPrice  
        form_class = EquipmentPriceForm  
        extra = 0
    
    class ChargePricesInline(InlineFormSet):  
        model = ChargePrice  
        form_class = ChargePriceForm  
        extra = 0
    
    class OfficeCreateView(CreateWithInlinesView):  
        inlines = [AssuranceFeaturePricesInline, EquipmentPricesInline, ChargePricesInline]  
    
    class OfficeUpdateView(UpdateWithInlinesView):  
        inlines = [AssuranceFeaturePricesInline, EquipmentPricesInline, ChargePricesInline]  
```

#### forms.py

\[sourcecode language="python" wraplines="false" collapse="false"\]  
class AssuranceFeaturePriceForm(forms.ModelForm):

class Meta:  
model = AssuranceFeaturePrice  
fields = ('id', 'office', 'feature', 'price')

@property  
def helper(self):  
helper = FormHelper()  
helper.label\_class = 'col-xs-4'  
helper.field\_class = 'col-xs-6'  
helper.form\_tag = False  
helper.layout = Layout(  
'id', 'office', 'feature', 'price',  
Div('DELETE', css\_class='hidden')  
)  
return helper

class EquipmentPriceForm(forms.ModelForm):

class Meta:  
model = EquipmentPrice  
fields = ('id', 'office', 'equipment', 'price')

@property  
def helper(self):  
helper = FormHelper()  
helper.label\_class = 'col-xs-4'  
helper.field\_class = 'col-xs-6'  
helper.form\_tag = False  
helper.layout = Layout(  
'id', 'office', 'equipment', 'price',  
Div('DELETE', css\_class='hidden')  
)  
return helper

class ChargePriceForm(forms.ModelForm):

class Meta:  
model = ChargePrice  
fields = ('id', 'office', 'charge', 'price')

@property  
def helper(self):  
helper = FormHelper()  
helper.label\_class = 'col-xs-4'  
helper.field\_class = 'col-xs-6'  
helper.form\_tag = False  
helper.layout = Layout(  
'id', 'office', 'charge', 'price',  
Div('DELETE', css\_class='hidden')  
)  
return helper

\[/sourcecode\]

**Template**:

\[sourcecode language="python" wraplines="false" collapse="false"\]  
\#\#\#\#\#\#\#\#\#\#\#\#  
\# template \#  
\#\#\#\#\#\#\#\#\#\#\#\#

{% block content2 %}  
{{ form.media }}

&lt;form id="form-office" method="post" action="{% if object %}{% url
update\_url smydestination object.pk %}{% else %}{% url create\_url
smydestination %}{% endif %}" class="form-horizontal"&gt;  
{{ form.errors }}  
{% crispy form %}  
&lt;!-- formsets --&gt;

&lt;div id="initial-precios" class="x\_panel col-md-offset-2
col-md-7"&gt;  
{% for formset in inlines %}

&lt;div id="container-{{ formset.prefix }}"&gt;

&lt;div class="x\_title"&gt;

&lt;h4&gt;{% show\_formset\_name formset %}&lt;/h4&gt;

&lt;/div&gt;

&lt;div class="formset well" data-formset-prefix="{{ formset.prefix
}}"&gt;

&lt;div class="errors"&gt;{{ formset.non\_form\_errors }}&lt;/div&gt;

{{ formset.management\_form }}

&lt;div data-formset-body&gt;  
{% for item in formset %}

&lt;div class="formset\_item form-inline" data-formset-form&gt;  
{% crispy item %}  
&lt;button type="button" data-formset-delete-button class="btn
btn-danger pull-right"&gt;&lt;i class="fa fa-trash"&gt;&lt;/i&gt; {%
trans 'Borrar' %}&lt;/button&gt;  
&lt;/div&gt;

{% endfor %}  
&lt;/div&gt;

&lt;script type="form-template" data-formset-empty-form&gt;  
{% escapescript %}

&lt;div class="formset\_item form-inline" data-formset-form&gt;  
{% crispy formset.empty\_form %}  
&lt;button type="button" data-formset-delete-button class="btn
btn-danger pull-right"&gt;&lt;i class="fa fa-trash"&gt;&lt;/i&gt; {%
trans 'Borrar' %}&lt;/button&gt;  
&lt;/div&gt;

{% endescapescript %}  
&lt;/script&gt;  
&lt;a class="btn btn-success" data-formset-add&gt;  
&lt;i class="fa fa-plus-square-o"&gt;&lt;/i&gt; {% trans 'Añadir
registro' %}  
&lt;/a&gt;  
&lt;/div&gt;

&lt;/div&gt;

{% endfor %}  
&lt;/div&gt;

&lt;!-- fin formsets --&gt;  
&lt;/form&gt;

{% endblock content2 %}

```djangotemplate
{% block extrajs %}  
<script type="text/javascript" src="{% static 'js/jquery.formset.min.js' %}"></script>  
<script type="text/javascript">  
//<![CDATA[ 
$(function($) { $(".formset").formset({
    animateForms: true, reorderMode: 'none', }); }); //\]\]>;  
</script>;  
{% endblock %}  
```

A aquest exemple també es fa ús de [Crispy Forms](http://django-crispy-forms.readthedocs.org/en/latest/), per tal
de millorar l'aparença dels formularis. Per instal.lar-ho:

    pip install --upgrade django-crispy-forms  

i afegir l'aplicació al projecte:  

```python
INSTALLED_APPS = (  
    ...  
    'crispy_forms',  
)  
```

En aquest cas hi ha varis "formsets" relacionats amb el model principal.
Per qüestió d'usabilitat s'ha implementat el formset dins un "Tab" del
formulari principal. L'exemple exposat queda segons es mostra a
l'imatge.

[![captura\_formsets\_cropped](http://www.espontas.com/wp-content/uploads/captura_formsets_cropped-1024x699.png){.alignleft
.size-large .wp-image-344 width="660"
height="451"}](http://www.espontas.com/wp-content/uploads/captura_formsets_cropped.png)

Per aprofondir en els paquets citats a l'exemple es recomana visitar els
enllaços als mateixos.
