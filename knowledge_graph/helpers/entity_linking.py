# Takes input text and runs it through DBpeadia's spotlight API https://www.dbpedia-spotlight.org/api and links the entity to DBpeadia
import requests
import pprint
from utils import exception

class EntityLinking:

    def entity_linking(self, input_text):
        spotlight_api_url = "https://api.dbpedia-spotlight.org/en/annotate"

        # /annotate API request payload
        request_payload = {
            "text": input_text,
            "confidence": 0.35
        }

        # /annotate API headers
        headers = {
            "accept": "application/json"
        }

        response = requests.get(url=spotlight_api_url, params=request_payload, headers=headers)
        if response.status_code != 200:
            raise exception.ExternalAPIExceptionError(response.status_code)

        result = response.json()
        pprint.pprint(result) # pretty print json

        return result


