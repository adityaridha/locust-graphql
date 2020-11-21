import json

import requests


def run_query(query):
    request = requests.post("http://countries.trevorblades.com/", json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.
query = """
{
  __schema {
    types {
      name
    }
  }
}
"""

result = run_query(query)  # Execute the query
print(json.dumps(result, indent=1))
