"""
Adds two Citation records, and for each of those, adds two CitationField records.
Can be run multiple times to add more records.
"""

import models_sqlalchemy
from models_sqlalchemy import Citation, CitationField


## make session
session = models_sqlalchemy.make_session()
assert session is not None


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

# Commit the changes to the database
session.commit()

# Close the session
session.close()

print('Records added successfully.')
