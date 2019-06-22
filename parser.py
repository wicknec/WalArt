#! /usr/bin/env python3

"""
parser
=======================


"""
# NOTE: the actual command documentation is collected from docstrings of the
# commands and is appended to __doc__ after the class has been defined.
"""
Revisions
=================
161117 created, add Code2Alib
161118 Node2Alib
"""
import WalArt

from ast import *
annotate_fields=True
include_attributes=False #line number etc
indent=''

#ref: https://bitbucket.org/takluyver/greentreesnakes/src/default/astpp.py?fileviewer=file-view-default
def _format(node, level=0):
    if isinstance(node, AST):
        fields = [(a, _format(b, level)) for a, b in iter_fields(node)]
        if include_attributes and node._attributes:
            fields.extend([(a, _format(getattr(node, a), level))
                           for a in node._attributes])
        return ''.join(['[',
            node.__class__.__name__,
            '|',
            ''.join(('[%s|%s]' % field for field in fields)
                       if annotate_fields else
                       (b for a, b in fields)),
            ']'])
    elif isinstance(node, list):
        lines = ['[|%s]'%_format(x,level+1) for x in node]
        return '[list|'+''.join(lines)+']'
    return repr(node)
def Node2Alib(node):
    if not isinstance(node, AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return WalArt.alib().FromString(_format(node))
    
def Code2Alib(code):
    return WalArt.alib().FromString(_format(parse(code)))
    
if __name__ == '__main__':
    print(CodeToAlib("['[|%s]'%_format(x,level+1) for x in node]").ToString(''))
    