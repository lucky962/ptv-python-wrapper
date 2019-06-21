from hashlib import sha1
import json
import hmac
import requests
import urllib

API_VER = '/v3/'
BASE_URL = 'http://timetableapi.ptv.vic.gov.au'

class PTVClient(object):
    """ Class to make calls to PTV Api """
    def __init__(self, dev_id, api_key):
        """
        Initialize a PTVClient

        Parameters
        ----------
        dev_id : str
            Developer ID from PTV
        api_key : str
            API key from PTV
        """
        self.dev_id = dev_id
        self.api_key = api_key

    def _calculateSignature(self, path):
        """
        Calculates a signature from url

        Parameters
        ----------
        path : str
            The target path of the url (e.g '/v3/search/')
        
        Returns
        -------
        signature : str
            The hex signature.
        """
        key = bytes(self.api_key, 'UTF-8')
        raw = bytes(path, 'UTF-8')
        return hmac.new(key, raw, sha1).hexdigest().upper()
        
    def _getUrl(self, path, params = {}):
        """
        Creates URL

        Parameters
        ----------
        path : str
            The target path of the url (e.g '/v3/search/')
        params : dict
            Dictionary containing parameters for request
                
        Returns
        -------
        url : str
            The url for the request
        """
        params['dev_id'] = self.dev_id
        query = "?" + urllib.parse.urlencode(params,doseq=True)
        url = BASE_URL + path + query + "$signature=" + self._calculateSignature(path + query)
        return url
        
    def _apiCall(self, path, params = {}): 
        """
        Calls API

        Parameters
        ----------
        path : str
            The target path of the url (e.g '/v3/search/')
        params : dict
            Dictionary containing parameters for request
        
        Returns
        -------
        response : dict
            Response of api call as dict
        """
        response = requests.get(self._getUrl(path, params))
        response.raise_for_status()
        return response.json()
        