Title: Afegir concurrència a comandes de Django
Date: 2018-06-02 10:41
Modified: 2018-06-02 10:41
Category: Django
Tags: django, concurrency
Slug: django-concurrency
Authors: Andreu

En algunes ocasions he hagut d'implementar alguna comanda de **Django** 
per tal de realitzar alguna tasca de manteniment. El procés sól esser, en moltes ocasions, el mateix. Processar secuencialment un número d'objectes. El problema és que quan s'executa la comanda es sol emprar un sol procés en un sol core. Això té l'inconvenient que, si el número d'objectes a tractar és molt gran, la comanda tarda considerablement.<!--more-->

Per posar un exemple. Una comanda que processa un model simple de Django amb 340.000 registres. L'operació a executar és comptar el número de paraules d'un camp de text i desar aquest número dins un camp del propi model. Emprant l'ORM de Django no ens permet d'executar l'operació al mateix temps que es llegeix, no podem fer un "update" executant una funció Python. Per aquest motiu, hem de, primer llegir el registre, calcular el número de paraules i llavors, en un segon pas, actualitzar el número de paraules sobre cada registre. D'aquesta manera ens queda que hem d'executar una sentència "update" d'sql per a cada registre.

Una possible implementació de la comanda podria esser la següent:

```python

# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
from ...models import TransTask
from ...utils import get_num_words


class Command(BaseCommand):
    help = "Update the number of words of the tasks"

    def handle(self, *args, **options):
        self.stdout.write('Reading tasks...')
        pairs = []
        for it in TransTask.objects.all():
            pairs.append({'id': it.id, 'num': get_num_words(it.object_field_value)})

        for item in pairs:
            TransTask.objects.filter(pk=item['id']).update(number_of_words=item['num'])

        self.stdout.write('end')

```


Emprant el suport per "<strong>Threads</strong>" de Python 3.4, una possible solució podria esser la següent:

```python

# -*- encoding: utf-8 -*-

from queue import Queue, Empty
from threading import Lock, Thread

from django.core.management.base import BaseCommand
from ...models import TransTask
from ...utils import get_num_words


class Command(BaseCommand):
    help = "Update the number of words of the tasks"

    lock = Lock()
    queue = Queue()
    num_threads = 80
    threads = []

    def handle(self, *args, **options):
        self.queue = Queue()
        self.stdout.write('Reading tasks...')
        for it in TransTask.objects.all():
            self.queue.put({'id': it.id, 'num': get_num_words(it.object_field_value)})

        for i in range(self.num_threads):
            t = Thread(target=self.worker_elements)
            t.start()
            self.threads.append(t)
        self.stdout.write("Waiting for empty queue")
        self.queue.join()
        self.stop_threads()

    def stop_threads(self):
        for t in self.threads:
            t.join()
        self.stdout.write('Exiting main thread')

    def worker_elements(self):
        while not self.queue.empty():
            try:
                item = self.queue.get(timeout=2)
                TransTask.objects.filter(pk=item['id']).update(number_of_words=item['num'])
            except Empty:
                break
            finally:
                self.queue.task_done()

```

Aquesta solució el que fá és, definir una cua ("<strong>Queue</strong>") a la quan anem desant els elements a processar i llavors definir una sèrie de "<strong>Threads</strong>", cadascún dels qual va desencuant els elements per tal de processar-los. D'aquesta manera aconseguim una "pseudo concurrència" a l'hora d'anar actualitzant la base de dades.

Per a processar un total d'uns 340.000 registres, la primera versió va tardar uns 22 min i 55 seg. Amb la segona versió, la multithreaded, va tardar 57 seg. Executades les dues versions amb la mateixa màquina i mateixes condicions.

Cal mencionar que, en realitat no estem afegint paralel.lisme, ja que només hi ha un thread executant-se a la vegada gràcies al <a href="https://wiki.python.org/moin/GlobalInterpreterLock" target="_blank">GIL</a> de Python. Aquest segon exemple és més ràpid ja que mentres un thread està esperant, per a mor de la connexió base de dades, s'arranca un altre thread que estigui disponible per processar un altre element.

Enllaços relacionats:

* <a href="http://www.tutorialspoint.com/python/python_multithreading.htm">http://www.tutorialspoint.com/python/python_multithreading.htm</a>
* <a href="http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python">http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python</a>
* <a href="http://www.tutorialspoint.com/python/python_multithreading.htm">http://www.tutorialspoint.com/python/python_multithreading.htm</a>



