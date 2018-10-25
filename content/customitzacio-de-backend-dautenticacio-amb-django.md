Title: Customització de backend d'autenticació amb Django
Date: 2015-12-30 10:11
Author: blogadmin
Category: Django, Feina
Slug: customitzacio-de-backend-dautenticacio-amb-django
Status: published

Per defecte Django empra el backend d'autenticació "ModelBackend"


    AUTHENTICATION\_BACKENDS = (  
        'django.contrib.auth.backends.ModelBackend',  
    )  

Aquest "backend" intenta autenticara partir del nom d'usuari i la
contrasenya que reb. Nogensmenys es pot donar el cas que vulguem
autenticar a partir de l'email de l'usuari.<!--more-->

Per aquest cas ho podem fer estenent la classe "ModelBackend" i
reimplementant el mètode autenticate:

    class MyCustomEmailAuthBackend(ModelBackend):  
        """  
        Allow users to log in with their email address  
        """
        
        def authenticate(self, email=None, password=None, \*\*kwargs):
            if email is None or password is None:  
                return None
            try:  
                user = User.objects.get(email=email)  
                if user.check_password(password):  
                    return user  
            except User.DoesNotExist:  
                return

Un cop que tenim el backend implementat l'hem d'afegir als "settings"
per tal que Django ho tingui en compte:
  
    AUTHENTICATION\_BACKENDS = (  
        'authentication.MyCustomEmailAuthBackend',  
        'django.contrib.auth.backends.ModelBackend',  
    )  
  
Aleshores si el nostre formulari posteja l'email i la contrasenya ja ens
podrem autenticar.
