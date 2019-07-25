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
        path = f"/v3/departures/route_type/{route_type}/stop/{stop_id}"
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
        path = f"/v3/directions/route/{route_id}"
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
        path = f"/v3/directions/{direction_id}"
        params = {}
        return self._callApi(path, params)
    
    def get_disruptions(self, route_id=None, stop_id=None, disruption_status=None):
        """
        View all disruptions
        
        Optional Parameters
        -------------------
        route_id : int
            Identifier of route; values returned by Routes API - v3/routes
        stop_id : int            	
            Identifier of stop; values returned by Stops API - v3/stops
        disruption_status : str
            Filter by status of disruption
        
        Returns
        -------
        disruptions : dict
            All disruption information (if any exists).
        """
        path = "/v3/disruptions"
        params = {}
        if route_id:
            path += f"/route/{route_id}"
        if stop_id:
            path += f"/stop/{stop_id}"
        if disruption_status:
            params['disruption_status'] = disruption_status
        return self._callApi(path, params)

    def get_disruption(self, disruption_id):
        """
        View a specific disruption

        Parameters
        ----------
        disruption_id : int
            Identifier of disruption; values returned by Disruptions API - /v3/disruptions OR /v3/disruptions/route/{route_id}
        
        Returns
        -------
        disruptions : dict
            Disruption information for the specified disruption ID.
        """
        path = f"/v3/disruptions/{disruption_id}"
        params = {}
        return self._callApi(path, params)

    def get_disruption_modes(self):
        """
        Get all disruption modes

        Returns
        -------
        modes : dict
            Disruption specific modes
        """
        path = "/v3/disruptions/modes"
        params = {}
        return self._callApi(path, params)
    
    def get_outlets(self, latitude=None, longitude=None, max_distance=None, max_results=None):
        """
        List all ticket outlets

        Optional Parameters
        -------------------
        latitude : int
            Geographic coordinate of latitude
        longitude : int
            Geographic coordinate of longitude
        max_distance : int
            Maximum number of results returned 
        max_results : int
            Maximum number of results returned (default = 30)
        
        Returns
        -------
        outlets : dict
            Ticket outlets
        """
        path = "/v3/outlets"
        params = {}
        if latitude and longitude:
            path += f"/location/{latitude},{longitude}"
        if max_distance:
            params['max_distance'] = max_distance
        if max_results:
            params['max_results'] = max_results
        return self._callApi(path, params)

    def get_pattern(self, run_id, route_type, expand, stop_id=None, date_utc=None):
        """
        View the stopping pattern for a specific trip/service run

        Parameters
        ----------
        run_id : int
            Identifier of a trip/service run; values returned by Runs API - /v3/route/{route_id} and Departures API
        route_type : int
            Number identifying transport mode; values returned via RouteTypes API
        expand : Array[str]
            Objects to be returned in full (i.e. expanded) - options include: all, stop, route, run, direction, disruption. By default disruptions are expanded.
        
        Optional Parameters
        -------------------
        stop_id : int
            Filter by stop_id; values returned by Stops API
        date_utc : str
            Filter by the date and time of the request (ISO 8601 UTC format)

        Returns
        -------
        pattern : dict
            The stopping pattern of the specified trip/service run and route type.
        """
        path = f"/v3/pattern/run/{run_id}/route_type/{route_type}"
        params = {}
        params['expand'] = expand
        if stop_id:
            params['stop_id'] = stop_id
        if date_utc:
            params['date_utc'] = date_utc
        return self._callApi(path, params)
    
    def get_routes(self, route_types=None, route_name=None):
        """
        View route names and numbers for all routes

        Optional Parameters
        -------------------
        route_types : Array[int]
            Filter by route_type; values returned via RouteTypes API
        route_name : str
            Filter by name of route (accepts partial route name matches)
        
        Returns
        -------
        routes : dict
            Route names and numbers for all routes of all route types.
        """
        path = "/v3/routes"
        params = {}
        if route_types:
            params['route_types'] = route_types
        if route_name:
            params['route_name'] = route_name
        return self._callApi(path, params)

    def get_route(self, route_id):
        """
        View route name and number for specific route ID

        Parameters
        ----------
        route_id : int
            Identifier of route; values returned by Departures, Directions and Disruptions APIs
        
        Returns
        -------
        route : dict
            The route name and number for the specified route ID.
        """
        path = f"/v3/routes/{route_id}"
        params = {}
        return self._callApi(path, params)

    def get_route_types(self):
        """
        View all route types and their names

        Returns
        -------
        RouteTypes : dict
            All route types (i.e. identifiers of transport modes) and their names.
        """
        path = "/v3/route_types"
        params = {}
        return self._callApi(path, params)
    
    def get_run(self, run_id, route_type=None):
        """
        View the trip/service for a specific run ID and route type

        Parameters
        ----------
        run_id : int
            Identifier of a trip/service run; values returned by Runs API - /v3/route/{route_id} and Departures API

        Optional Parameters
        -------------------
        route_type : int
            Number identifying transport mode; values returned via RouteTypes API

        Returns
        -------
        run : dict
            The trip/service run details for the run ID and route type specified.
        """
        path = f"/v3/runs/{run_id}"
        params = {}
        if route_type:
            path += f"/route_type/{route_type}"
        return self._callApi(path, params)

    def get_runs_for_route(self, route_id, route_type=None):
        """
        View all trip/service runs for a specific route ID

        Parameters
        ----------
        route_id : int
            Identifier of route; values returned by Routes API - v3/routes.

        Optional Parameters
        -------------------
        route_type : int
            Number identifying transport mode; values returned via RouteTypes API

        Returns
        -------
        runs : dict
            All trip/service run details for the specified route ID.
        """
        path = f"/v3/runs/route/{route_id}"
        params = {}
        if route_type:
            path += f"/route_type/{route_type}"
        return self._callApi(path, params)

    def search(self, search_term, route_types=None, latitude=None, longitude=None, max_distance=None, include_addresses=None, include_outlets=None, match_stop_by_suburb=None, match_route_by_suburb=None, match_stop_by_gtfs_stop_id=None):
        """
        View stops, routes and myki outlets that match the search term

        Parameters
        ----------
        search_term : str
            Search text (note: if search text is numeric and/or less than 3 characters, the API will only return routes)
        
        Optional Parameters
        -------------------
        route_types : Array[int]
            Filter by route_type; values returned via RouteTypes API (note: stops and routes are ordered by route_types specified)
        latitude : float
            Filter by geographic coordinate of latitude
        longitude : float
            Filter by geographic coordinate of longitude
        max_distance : float
            Filter by maximum distance (in metres) from location specified via latitude and longitude parameters
        include_addresses : bool
            Placeholder for future development; currently unavailable
        include_outlets : bool
            Indicates if outlets will be returned in response (default = true)
        match_stop_by_suburb : bool
            Indicates whether to find stops by suburbs in the search term (default = true)
        match_route_by_suburb : bool
            Indicates whether to find routes by suburbs in the search term (default = true)
        match_stop_by_gtfs_stop_id : bool
            Indicates whether to search for stops according to a metlink stop ID (default = false)
        
        Returns
        -------
        SearchResponse : dict
            Stops, routes and myki ticket outlets that contain the search term (note: stops and routes are ordered by route_type by default).
        """
        path = f"/v3/search/{urllib.parse.quote(search_term)}"
        params = {}
        if route_types:
            params['route_types'] = route_types
        if latitude:
            params['latitude'] = latitude
        if longitude:
            params['longitude'] = longitude
        if max_distance:
            params['max_distance'] = max_distance
        if include_addresses != None:
            params['include_addresses'] = str(include_addresses).lower()
        if include_outlets != None:
            params['include_outlets'] = str(include_outlets).lower()
        if match_stop_by_suburb != None:
            params['match_stop_by_suburb'] = str(match_stop_by_suburb).lower()
        if match_route_by_suburb != None:
            params['match_route_by_suburb'] = str(match_route_by_suburb).lower()
        if match_stop_by_gtfs_stop_id != None:
            params['match_stop_by_gtfs_stop_id'] = str(match_stop_by_gtfs_stop_id).lower()
        return self._callApi(path, params)

    def get_stop(self, stop_id, route_type, stop_location=None, stop_amenities=None, stop_accessibility=None, stop_contact=None, stop_ticket=None, gtfs=None, stop_staffing=None, stop_disruptions=None):
        """
        View facilities at a specific stop (Metro and V/Line stations only)

        Parameters
        ----------
        stop_id : int
            Identifier of stop; values returned by Stops API
        route_type : int
            Number identifying transport mode; values returned via RouteTypes API

        Optional Parameters
        -------------------
        stop_location : bool
            Indicates if stop location information will be returned (default = false)
        stop_amenities : bool  
            Indicates if stop amenity information will be returned (default = false)
        stop_accessibility : bool
            Indicates if stop accessibility information will be returned (default = false)
        stop_contact : bool
            Indicates if stop contact information will be returned (default = false)
        stop_ticket : bool
            Indicates if stop ticket information will be returned (default = false)
        gtfs : bool
            Incdicates whether the stop_id is a GTFS ID or not
        stop_staffing : bool
            Indicates if stop staffing information will be returned (default = false)
        stop_disruptions : bool
            Indicates if stop disruption information will be returned (default = false)

        Returns
        -------
        Stop : dict
            Stop location, amenity and accessibility facility information for the specified stop (metropolitan and V/Line stations only).
        """
        path = f"/v3/stops/{stop_id}/route_type/{route_type}"
        params = {}
        if stop_location != None:
            params['stop_location'] = str(stop_location).lower()
        if stop_amenities != None:
            params['stop_amenities'] = str(stop_amenities).lower()
        if stop_accessibility != None:
            params['stop_accessibility'] = str(stop_accessibility).lower()
        if stop_contact != None:
            params['stop_contact'] = str(stop_contact).lower()
        if stop_ticket != None:
            params['stop_ticket'] = str(stop_ticket).lower()
        if gtfs != None:
            params['gtfs'] = str(gtfs).lower()
        if stop_staffing != None:
            params['stop_staffing'] = str(stop_staffing).lower()
        if stop_disruptions != None:
            params['stop_disruptions'] = str(stop_disruptions).lower()
        return self._callApi(path, params)

    def get_stops_for_route(self, route_id, route_type, direction_id=None, stop_disruptions=None):
        """
        View all stops on a specific route

        Parameters
        ----------
        route_id : int
            Identifier of route; values returned by Routes API - v3/routes
        route_type : int
            Number identifying transport mode; values returned via RouteTypes API

        Optional Parameters
        -------------------
        direction_id : int
            An optional direction; values returned by Directions API. When this is set, stop sequence information is returned in the response.
        stop_disruptions : bool
            Indicates if stop disruption information will be returned (default = false)

        Returns
        -------
        stops : dict
            All stops on the specified route.
        """
        path = f"/v3/stops/route/{route_id}/route_type/{route_type}"
        params = {}
        if direction_id: 
            params['direction_id'] = direction_id
        if stop_disruptions:
            params['stop_disruptions'] = str(stop_disruptions).lower()
        return self._callApi(path, params)

    def get_stops_for_location(self, latitude, longitude, route_types=None, max_results=None, max_distance=None, stop_disruptions=None):
        """
        View all stops near a specific location

        Parameters
        ----------
        latitude : float
            Geographic coordinate of latitude
        longitude : float
            Geographic coordinate of longitude

        Optional Parameters
        -------------------
        route_types : Array[int]
            Filter by route_type; values returned via RouteTypes API
        max_results : int
            Maximum number of results returned (default = 30)
        max_distance : double  
            Filter by maximum distance (in metres) from location specified via latitude and longitude parameters (default = 300)
        stop_disruptions : bool
            Indicates if stop disruption information will be returned (default = false)

        Returns
        -------
        stops : dict
            All stops near the specified location.
        """
        path = f"/v3/stops/location/{latitude},{longitude}"
        params = {}
        if route_types:
            params['route_types'] = route_types
        if max_results:
            params['max_results'] = max_results
        if max_distance:
            params['max_distance'] = max_distance
        if stop_disruptions:
            params['stop_disruptions'] = stop_disruptions
        return self._callApi(path, params)
