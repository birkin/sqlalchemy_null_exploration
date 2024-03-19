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

import argparse, os, random
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
    pass

def update_data_01():
    """ Updates an existing citation_field entry.
        Does _not_ create new null values. """
    citation = session.query(Citation).filter_by(id=1).first()
    log.debug( f'citation, ``{citation}``' )
    citation_data = citation.citation_data
    log.debug( f'citation_data, ``{citation_data}``' )
    for citation_field_obj in citation_data:
        log.debug( f'citation_field_obj, ``{citation_field_obj}``' )
        log.debug( f'citation_field_obj.id, ``{citation_field_obj.id}``' )
        log.debug( f'citation_field_obj.citation_id, ``{citation_field_obj.citation_id}``' )
        log.debug( f'citation_field_obj.field_data, ``{citation_field_obj.field_data}``' )
        if citation_field_obj.id == 1:
            log.debug( 'updating data' )
            random_id = random.randint( 1000, 9999 )
            log.debug( f'random_id, ``{random_id}``' )
            citation_field_obj.field_data = f'newdata_{random_id}'
            session.commit()
            break
    return


def update_data_02():
    """ Updates an existing citation_field entry via a session.add() approach, mimic-ing the flow in the 
            assumed problem link at the top.
        Explanation (chatgpt4)...
            The session.add() method in SQLAlchemy is used to add an instance of a model to the session. 
            Its purpose is to queue the instance for insertion or update in the database when session.commit() is called. 
            However, when working with instances that are already part of a session, 
            especially those retrieved through a query, SQLAlchemy's session automatically tracks changes to those instances. 
            This is why you might not see an immediate difference in behavior whether you use session.add() explicitly 
            in your scenarios or not.
        Does _not_ create new null values; acts the same as update_data_01.
        """
    citation = session.query(Citation).filter_by(id=1).first()
    log.debug( f'citation, ``{citation}``' )
    citation_data = citation.citation_data
    log.debug( f'citation_data, ``{citation_data}``' )
    for citation_field_obj in citation_data:
        log.debug( f'citation_field_obj, ``{citation_field_obj}``' )
        log.debug( f'citation_field_obj.id, ``{citation_field_obj.id}``' )
        log.debug( f'citation_field_obj.citation_id, ``{citation_field_obj.citation_id}``' )
        log.debug( f'citation_field_obj.field_data, ``{citation_field_obj.field_data}``' )
        if citation_field_obj.id == 1:
            log.debug( 'updating data' )
            random_id = random.randint( 1000, 9999 )
            log.debug( f'random_id, ``{random_id}``' )
            citation_field_obj.field_data = f'newdata_{random_id}'
            session.add( citation_field_obj )
            session.add( citation )
            session.commit()
            break
    return

def update_data_03():
    """ TODO: mimic the flow in the assumed problem link at the top better.
        Instantiate a citation-field-object , link it to the existing citation, and then session.add() it.
        Maybe do that twice, _then_ session.commit().
    """
    # for i in range(2):
    #     cfield = models_alch.CitationField(
    #         citation_id=cite.id,
    #         field_id=zfield.id, 
    #         field_data=val
    #         )
    #     session.add(cfield)
    # session.add( cite )
    # session.commit()
    citation_obj = session.query(Citation).filter_by(id=1).first()
    for i in range(2):
        random_num = random.randint( 1000, 9999 )
        citation_field_obj = CitationField(
            citation_id=1,
            field_data=f'somenewdata_{random_num}' 
            )
        session.add( citation_field_obj )
    session.add( citation_obj )
    session.commit()
    log.info( 'check sqlite!' )
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='Process some arguments.' )
    parser.add_argument( '--arg', required=True, type=str, help='Argument to decide which function to call' )
    ## list args -----------------------------------
    args = parser.parse_args()
    log.debug( f'args, ``{args}``' )
    ## handle args ------------------------------
    if args.arg == 'list_citations':
        list_citations()
    elif args.arg == 'update_data_01':
        update_data_01()
    elif args.arg == 'update_data_02':
        update_data_02()
    elif args.arg == 'update_data_03':
        update_data_03()
    else:
        log.warning( f'No function matches the argument: {args.arg}' )
