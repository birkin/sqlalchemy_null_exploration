"""
Nothing here yet.

This is where I'm going to try to replicate both the NULL problem, and figure out a solution.

In the webapp, I see lots of entries like:

```
INSERT INTO `4_citation_fields` VALUES (181031,NULL,66,'2');
```

So that's:
- setting id to 181031
- setting citation_id to NULL   # THIS IS THE PROBLEM
- setting field_id to 66        # that's the zotero-field-id, not relevant here
- setting field_data to '2'

Plan to replicate problem:
- try to update the citation-field entries for a given citation.
- here's where I think the problem lies in the webapp (for citation-field):
  <https://github.com/Brown-University-Library/disa_dj_project/blob/41d964d2bbece86cc2649ef6042a07e535fc4d7b/disa_app/lib/v_data_document_manager.py#L145-L157>
"""


## setup ------------------------------------------------------------

## not working; sigh!
import logging
logging.getLogger('sqlalchemy.engine.base.Engine').setLevel( logging.WARNING )
logging.getLogger('sqlalchemy.engine.base').setLevel( logging.WARNING )
logging.getLogger('sqlalchemy.engine').setLevel( logging.WARNING )
logging.getLogger('sqlalchemy').setLevel( logging.WARNING )

import argparse, os
import models_sqlalchemy
from models_sqlalchemy import Citation, CitationField

## trying again; nope!
logging.getLogger('sqlalchemy.engine.base.Engine').setLevel( logging.WARNING )
logging.getLogger('sqlalchemy.engine.base').setLevel( logging.WARNING )
logging.getLogger('sqlalchemy.engine').setLevel( logging.WARNING )
logging.getLogger('sqlalchemy').setLevel( logging.WARNING )

## logging --------------------------------------
lglvl: str = os.environ.get( 'LOGLEVEL', 'DEBUG' )  # no envars configured yet, so it'll be 'DEBUG'
lglvldct = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO }
logging.basicConfig(
    level=lglvldct[lglvl],  # assigns the level-object to the level-key loaded from the envar
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger( __name__ )
log.debug( 'logging working' )

## make session ---------------------------------
session = models_sqlalchemy.make_session()
assert session is not None


## go to work -------------------------------------------------------

def list_citations():
    ## list citations
    citations = session.query(Citation).all()
    for citation in citations:
        log.debug( f'\n\ncitation, ``{citation}``' )
        log.debug( f'citation.id, ``{citation.id}``' )
        log.debug( f'citation.comments, ``{citation.comments}``' )
        log.debug( f'citation.acknowledgements, ``{citation.acknowledgements}``' )
        citation_data = citation.citation_data
        log.debug( f'citation_data, ``{citation_data}``' )
        for citation_field_obj in citation_data:
            log.debug( f'citation_field_obj, ``{citation_field_obj}``' )
            log.debug( f'citation_field_obj.id, ``{citation_field_obj.id}``' )
            log.debug( f'citation_field_obj.citation_id, ``{citation_field_obj.citation_id}``' )
            log.debug( f'citation_field_obj.field_data, ``{citation_field_obj.field_data}``' )
        # log.debug( f'citation.citation_data, ``{citation.citation_data}``' )
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='Process some arguments.' )
    parser.add_argument( '--arg', required=True, type=str, help='Argument to decide which function to call' )
    
    args = parser.parse_args()
    log.debug( f'args, ``{args}``' )
    
    if args.arg == 'list_citations':
        list_citations()
    elif args.arg == 'bar':
        # bar()
        pass
    else:
        print(f'No function matches the argument: {args.arg}')




    # cfield = models_sqlalchemy.CitationField( citation_id='foo', field_data='bar' )


# ## silence sqlalchemy logging
# """
# This is one of the earliest files loaded, so it's a good place to silence the sqlalchemy logging.
# """
# import logging
# logging.getLogger('sqlalchemy.engine.base.Engine').setLevel( logging.WARNING )
# logging.getLogger('sqlalchemy.engine.base').setLevel( logging.WARNING )
# logging.getLogger('sqlalchemy.engine').setLevel( logging.WARNING )