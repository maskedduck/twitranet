# -*- coding: utf-8 -*-
import unicodedata
import os, re
from django.http import HttpResponse
from django.template import RequestContext, add_to_builtins, loader, TemplateDoesNotExist
from django.conf import settings

re_hash=re.compile('(#+\w*)')
    
def strip_accents(s):
    s=unicode(s)
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def hashify(s):
    """Returns a cleaned version of given string.
    
    >>> hashify('azerty')
    azerty
    >>> hashify('aZerTy')
    azerty
    >>> hashify('azertyé')
    azertye            
    >>> hashify('aze rty')
    aze-rty
    """
    return strip_accents(s).lower().replace(' ','-')
    
def find_hashes(s):
    """Returns the list of hashes found in given string.
    
    >>> find_hashes('nothing here guys')
    []
    >>> find_hashes('may be #something here #guys')
    [u'something',u'guys']
    >>> find_hashes('may be #SOMETHING #weIrD here too')
    [u'something',u'weird']
    """
    l=re_hash.findall(s)
    return [hashify(x[1:]) for x in l]
    
def base_url(noslash=True):
    return "http://%s%s"%( os.environ['HTTP_HOST'], {False:'/', True:''}[noslash] )

def render_to_string(request, template_name, data=None):
    return loader.render_to_string(template_name, data,
        context_instance=RequestContext(request))

def render_to_response(request, template_name, data=None, mimetype=None):
    if mimetype is None:
        mimetype = settings.DEFAULT_CONTENT_TYPE
    if mimetype == 'application/xhtml+xml':
        # Internet Explorer only understands XHTML if it's served as text/html
        if request.META.get('HTTP_ACCEPT').find(mimetype) == -1:
            mimetype = 'text/html'
        # Since XHTML is served with two different MIME types, depending on the
        # browser, we need to tell proxies to serve different versions.
        from django.utils.cache import patch_vary_headers
        patch_vary_headers(response, ['User-Agent'])

    return HttpResponse(render_to_string(request, template_name, data),
        content_type='%s; charset=%s' % (mimetype, settings.DEFAULT_CHARSET))

def TextResponse(string=''):
    return HttpResponse(string,
        content_type='text/plain; charset=%s' % settings.DEFAULT_CHARSET)
