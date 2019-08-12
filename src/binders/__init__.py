#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To bind into ebooks
"""
import logging
import traceback

from .epub import make_epubs
from .web import make_webs
from .text import make_texts
from .calibre import make_calibres

logger = logging.Logger('BINDERS')

depends_on_none = [
    'text',
    'web',
    'epub',
]
depends_on_epub = [
    'docx',
    'mobi',
    'pdf',
    'rtf',
    'txt',
    'azw3',
    'fb2',
    'lit',
    'lrf',
    'oeb',
    'pdb',
    'pml',
    'rb',
    'snb',
    'tcr',
    'html',
]
available_formats = depends_on_none + depends_on_epub


def bind_books(app, data):
    if not app.output_formats:
        app.output_formats = {x: True for x in available_formats}
    # end if

    formats = []
    for x in depends_on_epub:
        if app.output_formats[x]:
            formats[:0] = [x]
            app.output_formats['epub'] = True
        # end if
    # end for
    for x in depends_on_none:
        if app.output_formats[x]:
            formats[:0] = [x]
        # end if
    # end for

    outputs = dict()
    for fmt in formats:
        try:
            if fmt == 'text':
                outputs[fmt] = make_texts(app, data)
            elif fmt == 'web':
                outputs[fmt] = make_webs(app, data)
            elif fmt == 'epub':
                outputs[fmt] = make_epubs(app, data)
            else:
                outputs[fmt] = make_calibres(app, outputs['epub'], fmt)
            # end if
        except Exception as err:
            logger.warn('Failed to generate "%s": %s' % (fmt, err))
            logger.debug(traceback.format_exc())
        # end try
    # end for
# end def