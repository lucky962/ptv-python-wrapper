from hashlib import sha1
import json
import hmac
import requests
import urllib

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
        params['devid'] = self.dev_id
        query = "?" + urllib.parse.urlencode(params,doseq=True)
        url = BASE_URL + path + query + "&signature=" + self._calculateSignature(path + query)
        return url
        
    def _callApi(self, path, params = {}): 
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
    
    def get_departures_from_stop(self, route_type, stop_id, route_id=None, platform_numbers=None, direction_id=None, look_backwards=None, gtfs=None, date_utc=None, max_results=None, include_cancelled = None, expand = None):
        """
        View departures from a stop

        Parameters
        ----------
        route_type : integer
            Number identifying transport mode; values returned via RouteTypes API
        stop_id : integer
            Identifier of stop; values returned by Stops API
        
        Optional Parameters
        -------------------
        route_id : string
            Identifier of route; values returned by RoutesAPI - v3/routes
        platform_numbers : Array[integer]
            Filter by platform number at stop
        direction_id : integer
            Filter by indentifier of direction of travel; values returned by Directions Api - /v3/directions/route/{route_id}
        look_backwards : boolean
            Indicates if filtering runs (and their departures) to those that arrive at destination before date_utc (default = false). Requires max_results > 0.
        gtfs : boolean
            Indicates that stop_id parameter will accept "GTFS stop_id" data
        date_utc : string
            Filter by the date and time of the request (ISO 8601 UTC format) (default = current date and time)
        max_results : integer
            Maximum number of results returned
        include_cancelled : boolean
            Indicates if cancelled services (if they exist) are returned (default = false) - metropolitan train only
        expand : Array[string]
            List objects to be returned in full (i.e. expanded) - options include: all, stop, route, run, direction, disruption

        Returns
        -------
        Departures : dict
            Dictionary of departures
        """
        path = "/v3/departures/route_type/{}/stop/{}"
        path = path.format(route_type,stop_id)
        params = {}
        if route_id:
            path += f"/route/{route_id}"
        if platform_numbers:
            params['platform_numbers'] = platform_numbers
        if direction_id:
            params['direction_id'] = direction_id
        if look_backwards:
            params['look_backwards'] = look_backwards
        if gtfs:
            params['gtfs'] = str(gtfs).lower()
        if date_utc:
            params['date_utc'] = date_utc
        if max_results:
            params['max_results'] = max_results
        if include_cancelled:
            params['include_cancelled'] = str(include_cancelled).lower()
        if expand:
            params['expand'] = str(expand).lower()
        return self._callApi(path, params)

    def get_direction_for_route(self, route_id, route_type=None):
        """
        View directions for route

        Parameters
        ----------
        route_id : int
            Identifier of route; values returned by Routes API - v3/routes
        
        Optional Parameters
        -------------------
        route_type : int
            Number identifying transport mode; values returned via RouteTypes API

        Returns
        -------
        Directions : dict
            The directions that a specified route travels in.
        """
        path = "/v3/directions/route/{}"
        path = path.format(route_id)
        params = {}
        if route_type:
            path += f"/route_type/{route_type}"
        return self._callApi(path, params)

    def get_route_for_direction(self, direction_id):
        """
        View all routes for direction.

        Parameters
        ----------
        direction_id : int
            Identifier of direction of travel; values returned by Directions API - /v3/directions/route/{route_id}
        
        Returns
        -------
        Routes : dict
            All routes that travel in the specified direction.
        """
        path = "/v3/directions/{}"
        path = path.format(direction_id)
        params = {}
        return self._callApi(path, params)
        