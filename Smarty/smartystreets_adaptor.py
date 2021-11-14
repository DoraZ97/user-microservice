import json

from address_services.smarty_address_service import *


class SmartyStreetsAdaptor:
    def __init__(self):
        pass

    @classmethod
    def get_api_keys(cls):
        smarty_info = context.get_context()
        print(smarty_info)
        auth_id = smarty_info["auth_id"]
        auth_token = smarty_info["auth_token"]

        return auth_id, auth_token

    @classmethod
    def get_credentials(cls):
        auth_id, auth_token = cls.get_api_keys()
        print(auth_id)
        credentials = StaticCredentials(auth_id, auth_token)
        return credentials

    @classmethod
    def do_lookup(cls, street_lookup):
        creds = cls.get_credentials()
        client = ClientBuilder(creds).with_licenses(["us-core-cloud"]).build_us_street_api_client()
        client.send_lookup(street_lookup)

        try:
            client.send_lookup(street_lookup)
        except exceptions.SmartyException as err:
            print(err)
            cls.candidates = None
            return

        cls.candidates = street_lookup.result
        first_candidate = cls.candidates[0]
        print("Address Components")
        print("-------------------")
        print("Primary number:  {}".format(first_candidate.components.primary_number))
        print("Predirection:	{}".format(first_candidate.components.street_predirection))
        print("Street name:	    {}".format(first_candidate.components.street_name))
        print("Street suffix:   {}".format(first_candidate.components.street_suffix))
        print("Postdirection:   {}".format(first_candidate.components.street_postdirection))
        print("City:			{}".format(first_candidate.components.city_name))
        print("State:		    {}".format(first_candidate.components.state_abbreviation))
        print("ZIP Code:		{}".format(first_candidate.components.zipcode))
        print("County:		    {}".format(first_candidate.metadata.county_name))
        print("Latitude:		{}".format(first_candidate.metadata.latitude))
        print("Longitude:	    {}".format(first_candidate.metadata.longitude))

    def do_search(self, city_dict):
        pass

    @classmethod
    def to_json(cls):
        pass