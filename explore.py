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

import argparse


def list_citations():
    print( 'will list citations' )
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='Process some arguments.' )
    parser.add_argument( '--arg', type=str, help='Argument to decide which function to call' )
    
    args = parser.parse_args()
    
    if args.arg == 'list_citations':
        list_citations()
    elif args.arg == 'bar':
        # bar()
        pass
    else:
        print(f'No function matches the argument: {args.arg}')




    # cfield = models_sqlalchemy.CitationField( citation_id='foo', field_data='bar' )
