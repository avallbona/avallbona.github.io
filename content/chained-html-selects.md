Title: Encadenar select's Html amb Django de manera fàcil i poc intrussiva
Date: 2018-06-03 10:41
Modified: 2018-06-03 10:41
Category: Django
Tags: django, html, javascript, jquery
Slug: chained-html-selects
Authors: Andreu


Fa un temps que he descobert un "plugin" jQuery que va força be per encadenar <em>select</em>'s Html amb Django, és a dir, que les opcións d'un <em>select</em> s'actualitzin en funció del valor seleccionat a un primer <em>select</em>. El "plugin" en qüestió és diu <strong><a href="http://www.appelsiini.net/projects/chained" target="_blank">Chained Selects Plugin for jQuery and Zepto</a></strong>. Per fer-lo servir simplement hem d'estendre el "widget" per defecte per representar els <em>select</em>'s html en Django.<!--more-->

La idea és crear codi html per tal que es mostri similar a la següent manera, és a dir, que la clau dels valors del primer select es fixin com a css class dels options del segon select.

```html
    <select id="mark" name="mark">
      <option value="">--</option>
      <option value="bmw">BMW</option>
      <option value="audi">Audi</option>
    </select>
    <select id="series" name="series">
      <option value="">--</option>
      <option value="series-3" class="bmw">3 series</option>
      <option value="series-5" class="bmw">5 series</option>
      <option value="series-6" class="bmw">6 series</option>
      <option value="a3" class="audi">A3</option>
      <option value="a4" class="audi">A4</option>
      <option value="a5" class="audi">A5</option>
    </select>
```

Aixi doncs per fer que aixo sigui possible en Django estendrem i customitzarem el widget <em>Select</em> que ve per defecte amb django.forms. 

```python

    # -*- encoding: utf-8 -*-

    from django.forms.widgets import Select
    from django.utils.encoding import force_text
    from django.utils.html import format_html
    from django.utils.safestring import mark_safe
    
    
    class CustomSelect(Select):
        """
        Custom widget used in combination with http://www.appelsiini.net/projects/chained
        in order to have two or more related html select's. Whenever the first select is changed updates
        the options of the related one
        """
    
        def render_option(self, selected_choices, option_value, option_label):
            if option_value is None or option_value == '':
                option_value = ''
                css_class = ''
            else:
                css_class, option_value = option_value.split('___')
    
            option_value = force_text(option_value)
    
            if option_value in selected_choices:
                selected_html = mark_safe(' selected="selected"')
                if not self.allow_multiple_selected:
                    # Only allow for a single selection.
                    selected_choices.remove(option_value)
            else:
                selected_html = ''
            return format_html('<option value="{0}"{1} class="{2}">{3}</option>', option_value, selected_html,
                               mark_safe(css_class), force_text(option_label))
```    
    

Llavors el nostre formulari ha de fer ús del "widget" customitzat. En el formulari hem de parar atenció als camps "group" i "type". El camp "type" depen del valor seleccionat a "group". Per a cada valor de "group" hi ha una sèrie de valors a "type". Cada cop que el select de "group" s'actualitzi, es canvii, es recalcularan els valors de "type". Aquesta és la clau del problema, el valor de l'option del segon selector ha d'esser processat per tal d'extreure'n el propi valor de l'option així com el valor de l'element pare dins el primer selector. És per això que al mètode __init__ del formulari customitzam l'atribut "choices" del widget del camp "type", per passar el valor en el format:

<code>clau-option-select-dependent__clau-option-valor-pare</code>

```python

class ProductFilter(FilterFormMixin, django_filters.FilterSet):

    by_name = django_filters.CharFilter(lookup_type='icontains', name='translations__name',
                                        required=False, label=_('Nombre'))

    code = django_filters.CharFilter(required=False, label=_('Código'))

    place = django_filters.ModelChoiceFilter(queryset=Place.objects.all(), required=False,
                                             empty_label=_('Todos los recintos'), name='product_places')

    group = django_filters.ModelChoiceFilter(queryset=GroupProductType.objects.all(), required=False,
                                             name='type__group', empty_label=_('Todos los grupos'))

    type = django_filters.ChoiceFilter(choices=(), required=False, label=_('Todos los tipos'))

    tags = NamedModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, label=_(u'Seleccione algún tag'))

    ENABLED_CHOICES = (
        ('all', _('Todos')),
        ('si', _('Activos')),
        ('no', _('Inactivos')),
    )
    enabled = django_filters.MethodFilter(required=False, label=_('Estado'),
                                          action='filter_enabled', widget=forms.Select(choices=ENABLED_CHOICES))

    @staticmethod
    def filter_enabled(queryset, value):
        if value == 'all':
            return queryset
        return queryset.filter(enabled=value == 'si')

    class Meta:
        model = Product
        fields = ('by_name', 'code', 'place', 'group', 'type', 'tags', 'enabled')

    def __init__(self, data=None, queryset=None, prefix=None, strict=None):

        choices = [('', _(u'Todos los tipos'))]
        choices += [('{0}___{1}'.format(it.group_id, it.pk), it.name) for it in ProductType.objects.order_by('name')]
        self.base_filters['type'].field.widget = CustomSelect(choices=choices)
        super().__init__(data, queryset, prefix, strict)

```

Per gestionar l'event del canvi hem de modificar el template que renderitza el formulari. D'aquesta manera incloem el Javascript necessari, el codi del propi plugin i el codi que s'encarrega de relacionar els dos selectors. 

```djangotemplate

{% block extrajs2 %}
    <script type="text/javascript" src="{% static 'bower_components/chained/jquery.chained.min.js' %}"></script>
    <script type="text/javascript">
        $(function(){
            $("#id_type").chained("#id_group");
        });
    </script>
{% endblock extrajs2 %}
```

A l'exemple li deim que el selector amb identificador "#id_type" depen del selector amb identificador "#id_group". Finalment senyalar que el plugin és bastant versàtil ja que permet enllaçar varis selectors a la vegada amb la mateixa tècnica. 

<a href="http://www.appelsiini.net/projects/chained">http://www.appelsiini.net/projects/chained</a>
