import models_sqlalchemy
from models_sqlalchemy import Citation, CitationField

# from models_sqlalchemy import Base, Citation, CitationField, engine

# Create the database tables based on the models if they don't already exist
# Base.metadata.create_all(engine)

# Create a new session
# session = make_session()
session = models_sqlalchemy.make_session()

# Add two Citation records
citation1 = Citation(comments='Dummy comment 1', acknowledgements='Dummy acknowledgement 1')
citation2 = Citation(comments='Dummy comment 2', acknowledgements='Dummy acknowledgement 2')

session.add(citation1)
session.add(citation2)

# Commit the citations to the database to get their generated ids
session.commit()

# Add two CitationField records for each Citation
citation_field1 = CitationField(citation_id=citation1.id)
citation_field2 = CitationField(citation_id=citation1.id)
citation_field3 = CitationField(citation_id=citation2.id)
citation_field4 = CitationField(citation_id=citation2.id)

session.add(citation_field1)
session.add(citation_field2)
session.add(citation_field3)
session.add(citation_field4)

# Commit the changes to the database
session.commit()

# Close the session
session.close()

print('Records added successfully.')
