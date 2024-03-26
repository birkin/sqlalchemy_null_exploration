"""
Updates records in an effort to replicate the db NULL problem -- then figure out a solution.

Started updating citation-data -- but wasn't able to recreate the NULL problem. 

The problem is most evident in location-data -- so trying that now.
"""


## setup ------------------------------------------------------------

## eliminating sqlalchemy-logging not working; sigh!
import logging
logging.getLogger('sqlalchemy.engine.base.Engine').setLevel( logging.WARNING )
logging.getLogger('sqlalchemy.engine.base').setLevel( logging.WARNING )
logging.getLogger('sqlalchemy.engine').setLevel( logging.WARNING )
logging.getLogger('sqlalchemy').setLevel( logging.WARNING )

import argparse, os, random
import models_sqlalchemy
from models_sqlalchemy import Citation, CitationField
from models_sqlalchemy import Reference, Location, ReferenceLocation

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


def list_locations():
    ## list locations
    log.debug( '\n\nSTART OF REFERENCE_LOCATION OUTPUT --------------' )
    reference_locations = session.query(ReferenceLocation).all()
    for reference_location in reference_locations:
        log.debug( f'\n\nreference_location, ``{reference_location}``' )
        log.debug( f'reference_location.id, ``{reference_location.id}``' )
        log.debug( f'reference_location.reference_id, ``{reference_location.reference_id}``' )
        log.debug( f'reference_location.location_id, ``{reference_location.location_id}``' )
        log.debug( f'reference_location.location, ``{reference_location.location}``' )
        log.debug( f'reference_location.location.id, ``{reference_location.location.id}``' )
        log.debug( f'reference_location.location.name, ``{reference_location.location.name}``' )
        # log.debug( f'reference_location.references, ``{reference_location.references}``' )  # does not work
        # log.debug( f'reference_location.location.references, ``{reference_location.location.references}``' )  # does work, showing ReferenceLogation objects
        # for loc_ref in reference_location.location.references:
        #     log.debug( f'loc_ref, ``{loc_ref}``' )
        #     log.debug( f'loc_ref.id, ``{loc_ref.id}``' )
        #     log.debug( f'loc_ref.reference_id, ``{loc_ref.reference_id}``' )
    log.debug( 'END OF REFERENCE_LOCATION OUTPUT' )

    log.debug( '\n\nSTART OF LOCATION OUTPUT ------------------------' )
    locations = session.query(Location).all()
    for location in locations:
        log.debug( f'\n\nlocation, ``{location}``' )
        log.debug( f'location.id, ``{location.id}``' )
        log.debug( f'location.name, ``{location.name}``' )
        log.debug( f'location.references, ``{location.references}``' )
        for loc_ref in location.references:
            log.debug( f'loc_ref, ``{loc_ref}``' )
            log.debug( f'loc_ref.id, ``{loc_ref.id}``' )
            log.debug( f'loc_ref.reference_id, ``{loc_ref.reference_id}``' )
            log.debug( f'loc_ref.reference.transcription, ``{loc_ref.reference.transcription}``' )
    log.debug( 'END OF LOCATION OUTPUT' )

    log.debug( '\n\nSTART OF REFERENCE OUTPUT ------------------------' )
    references = session.query(Reference).all()
    for reference in references:
        log.debug( f'\n\nreference, ``{reference}``' )
        log.debug( f'reference.id, ``{reference.id}``' )
        log.debug( f'reference.transcription, ``{reference.transcription}``' )
        log.debug( f'reference.locations, ``{reference.locations}``' )
        for ref_loc in reference.locations:
            log.debug( f'ref_loc, ``{ref_loc}``' )
            log.debug( f'ref_loc.id, ``{ref_loc.id}``' )
            log.debug( f'ref_loc.location_id, ``{ref_loc.location_id}``' )
            # log.debug( f'ref_loc.__dict__, ``{ref_loc.__dict__}``' )  # works
            # log.debug( f'ref_loc.location, ``{ref_loc.location}``' )  # works; yields object
            log.debug( f'ref_loc.location.name, ``{ref_loc.location.name}``' )
    log.debug( 'END OF REFERENCE OUTPUT' )
        
    pass





def update_citation_data_01():
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


def update_citation_data_02():
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

def update_citation_data_03():
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
    elif args.arg == 'list_locations':
        list_locations()
    elif args.arg == 'update_citation_data_01':
        update_citation_data_01()
    elif args.arg == 'update_citation_data_02':
        update_citation_data_02()
    elif args.arg == 'update_citation_data_03':
        update_citation_data_03()
    else:
        log.warning( f'No function matches the argument: {args.arg}' )
