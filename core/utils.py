# -*- coding: utf-8 -*-
import unicodedata
    
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
    string.find('')