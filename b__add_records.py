"""
Depending on arguments, adds citation-data or location-data to the database

location-data usage:
- cd /to/this/git-directory/
- source ../env/bin/activate
- python ./b__add_records.py --arg location_stuff

citationd-data usage:
- cd /to/this/git-directory/
- source ../env/bin/activate
- python ./b__add_records.py --arg citation_stuff

Adds two Citation records, and for each of those, adds two CitationField records.
Can be run multiple times to add more records.
"""

import argparse
import models_sqlalchemy
from models_sqlalchemy import Citation, CitationField
from models_sqlalchemy import Reference, Location, ReferenceLocation  # ReferenceLocation is the target '5_has_location' table


## make session
session = models_sqlalchemy.make_session()
assert session is not None


def add_location_data():

    ## add a Reference record
    reference1 = Reference( 
        id='1', 
        transcription='the transcription 01' 
        )
    session.add(reference1)

    ## commit reference so id is available
    session.commit()

    ## add a second Reference record
    reference2 = Reference( 
        id='2', 
        transcription='the transcription 02' 
        )
    session.add(reference2)

    ## commit reference so id is available
    session.commit()

    ## add a Location record
    location1 = Location( 
        id='1', 
        name='Location01' 
        )
    session.add(location1)

    ## commit location so id is available
    session.commit()

    ## add a second Location record
    location2 = Location( 
        id='2', 
        name='Location02' 
        )
    session.add(location2)

    ## commit location so id is available
    session.commit()

    # Add one ReferenceLocation record: 1st reference, 1st location
    reference_location1 = ReferenceLocation( 
        id='1',
        reference_id=reference1.id, 
        location_id=location1.id 
        )
    session.add(reference_location1)
    session.commit()

    # Add a second ReferenceLocation record: 2nd reference, 2nd location
    reference_location2 = ReferenceLocation( 
        id='2',
        reference_id=reference2.id, 
        location_id=location2.id 
        )
    session.add(reference_location2)
    session.commit()

    # Add a third ReferenceLocation record: 1st reference, 2nd location
    reference_location3 = ReferenceLocation( 
        id='3',
        reference_id=reference1.id, 
        location_id=location2.id 
        )
    session.add(reference_location2)
    session.commit()

    ## Close session
    session.close()

    print('location-data added successfully.')


def add_citation_data():

    ## add two Citation records
    citation1 = Citation(comments='Dummy comment 1', acknowledgements='Dummy acknowledgement 1')
    citation2 = Citation(comments='Dummy comment 2', acknowledgements='Dummy acknowledgement 2')

    session.add(citation1)
    session.add(citation2)

    ## commit citations so their ids are available
    session.commit()

    # Add two CitationField records for each Citation
    citation_field1 = CitationField( citation_id=citation1.id, field_data='Dummy field data 1.1' )
    citation_field2 = CitationField( citation_id=citation1.id, field_data='Dummy field data 1.2' )
    citation_field3 = CitationField( citation_id=citation2.id, field_data='Dummy field data 2.1' )
    citation_field4 = CitationField( citation_id=citation2.id, field_data='Dummy field data 2.2' )

    session.add(citation_field1)
    session.add(citation_field2)
    session.add(citation_field3)
    session.add(citation_field4)

    ## Commit changes 
    session.commit()

    ## Close session
    session.close()

    print('citation-data added successfully.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='Process some arguments.' )
    parser.add_argument( '--arg', required=True, type=str, help='Argument to decide which function to call' )
    ## list args -----------------------------------
    args = parser.parse_args()
    print( f'- args, ``{args}``' )
    ## handle args ------------------------------
    if args.arg == 'citation_data':
        add_citation_data()
    elif args.arg == 'location_data':
        add_location_data()
    else:
        print( f'- No function matches the argument: {args.arg}' )
