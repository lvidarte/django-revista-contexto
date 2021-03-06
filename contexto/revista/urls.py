# vim: set fileencoding=utf-8 :

from django.conf.urls.defaults import *
from contexto.revista.feeds import NotaFeeds
#from django.views.generic.simple import direct_to_template

urlpatterns = patterns('contexto.revista.views',

    (r'^feeds/$',
     NotaFeeds(), {},
     'contexto-revista-feeds'),

    (r'^autores/$',
     'listado_autores', {},
     'contexto-revista-autores'),

    (r'^autores/(?P<slug>[-\w]+)/((?P<page>\d+)/)?$',
     'listado_notas_autor', {},
     'contexto-revista-notas-autor'),

    (r'^tags/$',
     'listado_tags', {},
     'contexto-revista-tags'),

    (r'^tags/(?P<slug>[-\w]+)/((?P<page>\d+)/)?$',
     'listado_notas_tag', {},
     'contexto-revista-notas-tag'),

    (r'^paginas/(?P<url>.+)/$',
     'pagina', {},
     'contexto-revista-pagina'),

    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
     'nota', {},
     'contexto-revista-nota'),

    #(r'^$', 'pagina', {'url': 'proximamente'}, 'contexto-revista-portada'),
    (r'^((?P<page>\d+)/)?$',
     'portada', {},
     'contexto-revista-portada'),

)

