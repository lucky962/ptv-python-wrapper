# ptv-python-wrapper
A python API Wrapper for Public Transport Victoria (PTV)

## Usage
Instantiate client by passing in Developer ID and API Key from PTV
```
from ptv.client import PTVClient

client = PTVClient(DEV_ID, API_KEY)
```

### Get Departures from Stop
View departures from a stop
```
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
```
Example:
```
client.get_departure_from_stop(0, 1071)
```

### Get Directions for Route
View directions for route
```
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
    Dictionary of directions
```
Example:
```
client.get_directions_for_route(1)
```

### Get Route for Direction
View Routes for Direction
```
Parameters
----------
direction_id : int
    Identifier of direction of travel; values returned by Directions API - /v3/directions/route/{route_id}

Returns
-------
Routes : dict
    All routes that travel in the specified direction.
```
Example:
```
client.get_route_for_direction(1)
```

### Get Disruptions
View all disruptions
```
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
```
Example
```
client.get_disruptions()
```

## Progress
This is a work-in-progress api wrapper

The things we are working on:
- [x] Api Calling
    - [x] Calculate Signature
    - [x] Get Url
    - [x] Call Api
- [x] Departures
    - [x] View departures for all routes from a stop
    - [x] View departures for a specific route from a stop
- [x] Directions
    - [x] View directions that a route travels in
    - [x] View all routes for a directino of travel
    - [x] View all routes of a particular type for a direction of travel
- [ ] Disruptions
    - [x] View all disruptions for all route types
    - [x] View all disruptions for a particular route
    - [x] View all disruptions for a particular route and stop
    - [x] View all disruptions for a particular stop
    - [ ] View a specific disruption
    - [ ] Get all disruptions modes
- [ ] Outlets
    - [ ] List all ticket outlets
    - [ ] List ticket outlets near a specific location
- [ ] Patterns
    - [ ] View the stopping pattern for a specific trip/service run
- [ ] Routes
    - [ ] View route names and numbers for all routes
    - [ ] View route name and number for specific route ID
- [ ] RouteTypes
    - [ ] View all route types and their names
- [ ] Runs
    - [ ] View all trip/service runs for a specific route ID
    - [ ] View all trip/service runs for a specific route ID and route type
    - [ ] View all trip/service runs for a specific run ID
    - [ ] View the trip/service runs for a specific run ID and route type
- [ ] Search
    - [ ] View stops, routes and myki ticket outlets that match the search term
- [ ] Stops
    - [ ] View facilities at a specific stop (Metro and V/Line stations only)
    - [ ] View all stops on a specific route
    - [ ] View all stops near a specific location
- [ ] Other
    - [ ] Documentation
    