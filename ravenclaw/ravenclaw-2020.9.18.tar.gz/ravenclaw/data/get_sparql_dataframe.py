# source: https://lawlesst.github.io/notebook/sparql-dataframe.html
import pandas as pd
import json
from SPARQLWrapper import SPARQLWrapper, JSON

def get_sparql_dataframe(query, service = "https://query.wikidata.org/sparql"):
    """
    Helper function to convert SPARQL results into a Pandas data frame.
    """
    sparql = SPARQLWrapper(service)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = sparql.query()

    processed_results = json.load(result.response)
    cols = processed_results['head']['vars']

    out = []
    for row in processed_results['results']['bindings']:
        item = []
        for c in cols:
            item.append(row.get(c, {}).get('value'))
        out.append(item)

    return pd.DataFrame(out, columns=cols)