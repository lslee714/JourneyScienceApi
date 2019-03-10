import pandas as pd

def chunkify_big_json(json, chunkSize=10):
    """Generator for chunkifying a big json file"""
    jsonReader = pd.read_json(json, lines=True, chunksize=chunkSize, compression='infer')
    for chunk in jsonReader:
        yield chunk