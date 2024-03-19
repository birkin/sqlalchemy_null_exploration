import sqlalchemy
from sqlalchemy import Boolean, Float, Integer, String, ForeignKey, DateTime, UnicodeText
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  # one of the ways to define mapping between python classes and db-tables
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, scoped_session



Base = declarative_base()   # base class contains a MetaData object where newly defined Table objects are collected. 
                            # This collection is what SQLAlchemy uses to create the schema in the database.
                            # Each model will then be able to inherit from Base, 
                            # gaining the ability to interact with the database through the SQLAlchemy session interface.


DATABASE_URL="sqlite:///../DBs/DISA.sqlite"


## session configuration --------------------------------------------

"""
This implements a `singleton-pattern` for the SQLAlchemy engine and scoped_session, 
ensuring that these objects are instantiated only once.

The `scoped_session` exists only for the duration of a request, and is then removed.
"""
engine = None
ScopedSession = None

def initialize_engine_session():
    global engine, ScopedSession
    if engine is None:
        engine = create_engine( DATABASE_URL, echo=True )

        ## silence sqlalchemy logging; unsuccessful -- TODO: figure out how to silence sqlalchemy logging
        import logging
        logging.getLogger('sqlalchemy.engine.base.Engine').setLevel( logging.WARNING )
        logging.getLogger('sqlalchemy.engine.base').setLevel( logging.WARNING )
        logging.getLogger('sqlalchemy.engine').setLevel( logging.WARNING )
        logging.getLogger('sqlalchemy.orm.unitofwork').setLevel( logging.WARNING )
        logging.getLogger('sqlalchemy.orm').setLevel( logging.WARNING )
        logging.getLogger('sqlalchemy.pool.impl').setLevel( logging.WARNING )
        logging.getLogger('sqlalchemy.pool').setLevel( logging.WARNING )
        logging.getLogger('sqlalchemy').setLevel( logging.WARNING )
        
        session_factory = sessionmaker( bind=engine )
        ScopedSession = scoped_session( session_factory )
        return engine

def make_session():
    """
    Call this function to get a thread-local session
    for the current thread, initializing the engine and session factory
    if they haven't been initialized yet.
    """
    if engine is None or ScopedSession is None:
        initialize_engine_session()
    return ScopedSession

## END session configuration ----------------------------------------


## citation data start ----------------------------------------------


class Citation( Base ):
    __tablename__ = '3_citations'

    id = Column(Integer, primary_key=True)
    comments = Column(UnicodeText())
    acknowledgements = Column(String(255))

    def __repr__(self):
        return '<Citation {0}>'.format(self.id)


class CitationField( Base ):
    __tablename__ = '4_citation_fields'

    id = Column(Integer, primary_key=True)
    citation_id = Column(Integer, ForeignKey('3_citations.id'))
    citation = relationship(Citation,
        primaryjoin=(citation_id == Citation.id),
        backref='citation_data')
    field_data = Column(String(255))


## citation data end ------------------------------------------------
    

## reference data start ---------------------------------------------


class Reference( Base ):
    __tablename__ = '4_references'

    id = Column(Integer, primary_key=True)
    transcription = Column(UnicodeText())

    def __repr__(self):
        return '<Reference {0}>'.format(self.id)
    

class Location(Base):
    __tablename__ = '1_locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    # origin_for = relationship('Referent',
    #     secondary=has_origin, back_populates='origins')

    def __repr__(self):
        return '<Location {0}: {1}>'.format(self.id, self.name)


class ReferenceLocation( Base ):
    __tablename__ = '5_has_location'

    id = Column(Integer, primary_key=True)
    reference_id = Column(Integer, ForeignKey('4_references.id'))
    reference = relationship(Reference,
        primaryjoin=(reference_id == Reference.id),
        backref='locations')
    location_id = Column(Integer, ForeignKey('1_locations.id'))
    location = relationship(Location,
        primaryjoin=(location_id == Location.id),
        backref='references')
    # location_type_id = Column(Integer, ForeignKey('1_location_types.id'))
    # location_rank = Column(Integer)


## reference data end -----------------------------------------------


## for reference ----------------------------------------------------
    
# class Reference(Base):
#     __tablename__ = '4_references'

#     id = Column(Integer, primary_key=True)
#     citation_id = Column(Integer, ForeignKey('3_citations.id'),
#         nullable=False)
#     reference_type_id = Column(Integer, ForeignKey('1_reference_types.id'),
#         nullable=False)
#     national_context_id = Column(Integer, ForeignKey('1_national_context.id'),
#         nullable=False)
#     date = Column(DateTime())
#     transcription = Column(UnicodeText())
#     image_url = Column( String(500) )
#     referents = relationship(
#         'Referent', backref='reference', lazy=True, cascade="delete")
#     groups = relationship(
#         'Group', backref='reference', lazy=True, cascade="delete")

#     def last_edit(self):
#         """ Note: self.edits is possible because of ReferenceEdit() """
#         edits: list[tuple] = sorted([ (e.timestamp, e) for e in self.edits ],
#              key=operator.itemgetter(0), reverse=True)
#         log.debug( f'edits, ```{edits}```' )
#         if edits:
#             return_edits = edits[0][1]
#         else:
#             return_edits = None
#         log.debug( f'return_edits, ``{return_edits}``' )
#         log.debug( f'type(return_edits), ``{type(return_edits)}``' )
#         return return_edits

#     def display_date(self):
#         if self.date:
#             return self.date.strftime('%Y %B %d')
#         else:
#             return ''

#     def display_location_info( self ):
#         # session = make_session()
#         locations_lst = []
#         rfrnc_locations = self.locations
#         log.debug( f'rfrnc_locations, ```{rfrnc_locations}```' )
#         for rfrnc_location in rfrnc_locations:
#             location_name = rfrnc_location.location.name
#             location_type = None
#             try:
#                 location_type = rfrnc_location.location_type.name
#             except:
#                 log.exception( f'problem parsing rfrnc_location, ```{rfrnc_location.__dict__}```; traceback follows; processing will continue' )
#             loc_dct = { 'location_name': location_name, 'location_type': location_type }
#             log.debug( f'loc_dct, ```{loc_dct}```' )
#             locations_lst.append( loc_dct )
#         return locations_lst

#     def dictify( self ):
#         if self.date:
#             datetime_obj = cast( datetime.datetime, self.date )
#             isodate = datetime.date.isoformat( datetime_obj )
#         else:
#             isodate = ''
#         jsn_referents = []
#         for rfrnt in self.referents:
#             jsn_referents.append( {'id': rfrnt.id, 'age': rfrnt.age, 'sex': rfrnt.sex} )
#         last_edit = self.last_edit()
#         if last_edit:
#             last_edit_str: str = last_edit.timestamp.strftime( '%Y-%m-%d' )
#         else: 
#             last_edit_str = ''
#         data = {
#             'id': self.id,
#             'citation_id': self.citation_id,
#             'reference_type_id': self.reference_type_id,
#             'reference_type_name': self.reference_type.name,  # NB: this appears to be an sqlalchemy convention -- that if there is a ForeignKey, I can just go ahead and refernce the property name.
#             'national_context_id': self.national_context_id,
#             'date': isodate,
#             'transcription': self.transcription,
#             'referents': jsn_referents,
#             'last_edit': last_edit_str,
#             'location_info': self.display_location_info()
#             }
#         return data

#     def __repr__(self):
#         return '<Reference {0}>'.format(self.id)
    
#     ## end class Reference() ----------------------------------------


# class ReferenceLocation(Base):
#     __tablename__ = '5_has_location'

#     id = Column(Integer, primary_key=True)
#     reference_id = Column(Integer, ForeignKey('4_references.id'))
#     location_id = Column(Integer, ForeignKey('1_locations.id'))
#     location_type_id = Column(Integer, ForeignKey('1_location_types.id'))
#     location_rank = Column(Integer)
#     reference = relationship(Reference,
#         primaryjoin=(reference_id == Reference.id),
#         backref='locations')
#     location = relationship(Location,
#         primaryjoin=(location_id == Location.id),
#         backref='references')



# class CitationField(Base):
#     __tablename__ = '4_citation_fields'

#     id = Column(Integer, primary_key=True)
#     citation_id = Column(Integer, ForeignKey('3_citations.id'))
#     field_id = Column(Integer, ForeignKey('1_zotero_fields.id'))
#     field_data = Column(String(255))
#     citation = relationship(Citation,
#         primaryjoin=(citation_id == Citation.id),
#         backref='citation_data')
#     field = relationship(ZoteroField,
#         primaryjoin=(field_id == ZoteroField.id),
#         backref='citations')
    

# class Citation(Base):
#     __tablename__ = '3_citations'

#     id = Column(Integer, primary_key=True)

#     # uuid = Column( String(32) )

#     citation_type_id = Column(Integer, ForeignKey('2_citation_types.id'),
#         nullable=False)
#     display = Column(String(500))
#     zotero_id = Column(String(255))
#     comments = Column(UnicodeText())
#     acknowledgements = Column(String(255))
#     references = relationship('Reference', backref='citation', lazy=True)

#     def dictify( self ):  # branch new_flow, 2021-Apr-01
#         jsn_references = []
#         for rfrnc in self.references:
#             jsn_references.append( rfrnc.dictify() )
#         data = {
#             'id': self.id,
#             'citation_type_id': self.citation_type_id,
#             'citation_type_name': self.citation_type.name,
#             'display': self.display,
#             'zotero_id': self.zotero_id,
#             'comments': self.comments,
#             'acknowledgements': self.acknowledgements,
#             'references': jsn_references,
#             'fields': { f.field.name: f.field_data for f in self.citation_data }  # note: `citation_data` is the "backref" from class CitationField() `citation` (whew!).
#             }
#         return data

#     def __repr__(self):
#         return '<Citation {0}>'.format(self.id)
