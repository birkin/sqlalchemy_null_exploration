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
