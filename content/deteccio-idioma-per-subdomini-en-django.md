Title: Detecció idioma per subdomini en Django
Date: 2015-12-30 11:20
Author: blogadmin
Category: Django, Feina
Slug: deteccio-idioma-per-subdomini-en-django
Status: published

Django ens proporciona eines per detectar i fixar l'idioma de la nostra
aplicació. Normalment es fa servir
**[i18n\_patterns](https://docs.djangoproject.com/en/1.9/topics/i18n/translation/)**
a través del qual s'encapsulen les urls amb el mateix per tal que ens
fixi a l'inici del path de la url el codi d'idioma. Amb el middleware
que explicarem no cal fer servir l'**i18n\_patterns** ja que serà el
pròpi "middleware" que detectarà i fixarà l'idioma de l'aplicació.
<!--more-->

Primer de tot crearem l'arxiu que contindrà el "middleware":

\[sourcecode language="python"\]

\# -\*- encoding: utf-8 -\*-

from django.utils import translation  
from django.conf import settings

class SubdomainLanguageMiddleware(object):  
"""  
Set the language for the site based on the subdomain the request  
is being served on. For example, serving on 'fr.domain.com' would  
make the language French (fr).  
"""  
language\_codes = \[it\[0\] for it in settings.LANGUAGES\]

def process\_request(self, request):  
try:  
lang = request.get\_host().split('.')\[0\]  
except IndexError:  
lang = self.language\_codes\[0\]  
if lang == 'www':  
lang = self.language\_codes\[0\]  
if lang and lang in self.language\_codes:  
translation.activate(lang)  
request.LANGUAGE\_CODE = lang

\[/sourcecode\]

Fixem-nos en el cas que no s'ens indica cap codi d'idioma i ens ve
"www", que fixem el primer idioma per defecte definit als "settings.py".

Llavors, als "settings.py" hem de tenir configurats els idiomes amb els
quals volem fer feina:

\[sourcecode language="python"\]  
LANGUAGES = (  
('ca', 'Català'),  
('es', 'Español'),  
('de', 'Deutsch'),  
('en', 'English'),  
)  
\[/sourcecode\]

i, com a darrer pas, li hem d'indicar als "settings.py" que ens agafi el
"middleware" que acabem de crear:

\[sourcecode language="python"\]  
MIDDLEWARE\_CLASSES = (  
...,  
'myproject.language\_middleware.SubdomainLanguageMiddleware',  
)  
\[/sourcecode\]

Llavors ja podrem accedir a la web fixant l'idioma en el subdomini:

\[sourcecode language="html"\]  
http://www.lamevaweb.com  
http://es.lamevaweb.com  
http://de.lamevaweb.com  
http://en.lamevaweb.com  
\[/sourcecode\]
