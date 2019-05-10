Title: ManyToManyFields with a Through Model
Date: 2019-05-10 23:12
Modified: 2019-05-10 23:12
Category: Django 
Tags: django, django-rest-framework, rest, api
Slug: manytomanyfields-with-a-through-model
Authors: Andreu

Many times I found myself, many collegues and some [other people][stackoverflow] struggling 
when working with **ManyToManyFields** and trying to serialize 
the relation with a **Through** Model.<!--more-->

I think the official documentation of the amazing [django-rest-framework][django-rest-framework] does not provide 
a clear example on how to do it (may be it's a to specific use case). So I decided to leave here, as a reminder 
to myself and to anybody else, a small clarifitacion on how it works.

Example, given the following models:

    class Artist(models.Model):
        name = models.CharField(max_length=180)
    
        def __str__(self):
            return self.name
    
    
    class Portfolio(models.Model):
        user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
        name = models.CharField(max_length=180)
        artists = models.ManyToManyField(Artist, through='Calification')
    
        def __str__(self):
            return '{} - {}'.format(self.user, self.name)
    
    
    class Calification(models.Model):
        portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='califications')
        artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
        rate = models.IntegerField(default=0)
        added_at = models.DateTimeField(auto_now_add=True)
    
        def __str__(self):
            return '{} - {} - {}'.format(self.portfolio, self.artist, self.rate)
    
We could serialize them as follows:

    class ArtistSerializer(serializers.ModelSerializer):

        class Meta:
            model = Artist
            fields = ('name', )
    
    
    class CalificationSerializer(serializers.ModelSerializer):
    
        artist = ArtistSerializer()
    
        class Meta:
            model = Calification
            fields = ('artist', 'rate', 'added_at')
    
    
    class PortfolioSerializer(serializers.ModelSerializer):
    
        artists = CalificationSerializer(many=True, source='califications')
    
        class Meta:
            model = Portfolio
            fields = ('id', 'name', 'user', 'artists', )
            

It's important to remember that it's easier if we set a ``related_name`` to the foreign_key we want to follow from the main model.
If we don't set it we would have to set the attribute ``source`` of the nested serializer ``CalificationSerializer`` as

    artists = CalificationSerializer(many=True, source='calification_set.all') 

By default, relational fields that target a ``ManyToManyField`` with a
``through`` model specified are set to read-only.

If you explicitly specify a relational field pointing to a
``ManyToManyField`` with a through model, be sure to set ``read_only``
to ``True``.


[django-rest-framework]: https://www.django-rest-framework.org/api-guide/relations/#manytomanyfields-with-a-through-model
[stackoverflow]: https://stackoverflow.com/questions/17256724/include-intermediary-through-model-in-responses-in-django-rest-framework