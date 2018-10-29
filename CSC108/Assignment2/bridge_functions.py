""" 
Assignment 2: Bridges

The data used for this assignment is a subset of the data found in:
https://www.ontario.ca/data/bridge-conditions
"""

import csv
import math
from typing import List, TextIO

ID_INDEX = 0
NAME_INDEX = 1
HIGHWAY_INDEX = 2
LAT_INDEX = 3
LON_INDEX = 4
YEAR_INDEX = 5
LAST_MAJOR_INDEX = 6
LAST_MINOR_INDEX = 7
NUM_SPANS_INDEX = 8
SPAN_LENGTH_INDEX = 9
LENGTH_INDEX = 10
LAST_INSPECTED_INDEX = 11
BCIS_INDEX = 12

HIGH_PRIORITY_BCI = 60   
MEDIUM_PRIORITY_BCI = 70
LOW_PRIORITY_BCI = 100

HIGH_PRIORITY_RADIUS = 500  
MEDIUM_PRIORITY_RADIUS = 250
LOW_PRIORITY_RADIUS = 100

EARTH_RADIUS = 6371

####### BEGIN HELPER FUNCTIONS ####################

def read_data(csv_file: TextIO) -> List[List[str]]:
    """Read and return the contents of the open CSV file csv_file as a list of
    lists, where each inner list contains the values from one line of csv_file.

    Docstring examples not given since results depend on csv_file.
    """ 

    data = []
    lines = csv.reader(csv_file)
    for line in lines:            
        data.append(line)
    data = data[2:]
    return data


def calculate_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined by   
    (lat1, lon1) and (lat2, lon2), rounded to the nearest meter.
    
    >>> calculate_distance(43.659777, -79.397383, 43.657129, -79.399439)
    0.338
    >>> calculate_distance(43.42, -79.24, 53.32, -113.30)
    2713.226
    """

    # This function uses the haversine function to find the
    # distance between two locations. You do NOT need to understand why it
    # works. You will just need to call on the function and work with what it
    # returns.
    # Based on code at goo.gl/JrPG4j

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = (math.radians(lon1), math.radians(lat1), 
                              math.radians(lon2), math.radians(lat2))

    # haversine formula t
    lon_diff = lon2 - lon1 
    lat_diff = lat2 - lat1 
    a = (math.sin(lat_diff / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    return round(c * EARTH_RADIUS, 3)


####### END HELPER FUNCTIONS ####################

### SAMPLE DATA TO USE IN DOCSTRING EXAMPLES ####

THREE_BRIDGES_UNCLEANED = [
    ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403', '43.167233',
     '-80.275567', '1965', '2014', '2009', '4',
     'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012', '72.3', '',
     '72.3', '', '69.5', '', '70', '', '70.3', '', '70.5', '', '70.7', '72.9',
     ''],
    ['1 -  43/', 'WEST STREET UNDERPASS', '403', '43.164531', '-80.251582',
     '1963', '2014', '2007', '4',
     'Total=60.4  (1)=12.2;(2)=18;(3)=18;(4)=12.2;', '61', '04/13/2012',
     '71.5', '', '71.5', '', '68.1', '', '69', '', '69.4', '', '69.4', '',
     '70.3', '73.3', ''],
    ['2 -   4/', 'STOKES RIVER BRIDGE', '6', '45.036739', '-81.33579', '1958',
     '2013', '', '1', 'Total=16  (1)=16;', '18.4', '08/28/2013', '85.1',
     '85.1', '', '67.8', '', '67.4', '', '69.2', '70', '70.5', '', '75.1', '',
     '90.1', '']
    ]

THREE_BRIDGES = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,
                  -80.275567, '1965', '2014', '2009', 4,
                  [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
                 [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
                  '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61.0, 
                  '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3,
                                 73.3]],
                 [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, '1958',
                  '2013', '', 1, [16.0], 18.4, '08/28/2013',
                  [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]
                ]

#################################################
def format_data(data: List[List[str]]) -> None:  
    """Modify data so that it follows the format outlined in the 
    'Data formatting' section of the assignment handout.
    
    >>> d = THREE_BRIDGES_UNCLEANED
    >>> format_data(d)
    >>> d == THREE_BRIDGES
    True
    """

    i = 1
    for items in data:
        items[ID_INDEX] = i
        i += 1
        items[LAT_INDEX] = float(items[LAT_INDEX])
        items[LON_INDEX] = float(items[LON_INDEX])
        items[NUM_SPANS_INDEX] = int(items[NUM_SPANS_INDEX])
        num = items[SPAN_LENGTH_INDEX].count(";")
        new_span = items[SPAN_LENGTH_INDEX]
        span_length = []
        for j in range(num):
            ind1 = new_span.find(")")
            ind2 = new_span.find(";")
            span_length.append(float(new_span[ind1 + 2:ind2]))
            new_span = new_span[ind2+1:]
            j += 1
        items[SPAN_LENGTH_INDEX] = span_length
        items[LENGTH_INDEX] = float(items[LENGTH_INDEX])
        bcis = items[LAST_INSPECTED_INDEX + 2:]
        new_bcis = []
        k = 0
        while k < len(bcis):
            abc = bcis[k]
            if abc != "":
                bci = float(abc)
                new_bcis.append(bci)
            k += 1
        items[BCIS_INDEX] = new_bcis
        items[:] = items[:BCIS_INDEX + 1]


def get_bridge(bridge_data: List[list], bridge_id: int) -> list:
    """Return the data for the bridge with id bridge_id from bridge_data. If
    there is no bridge with the given id, return an empty list.  
    
    >>> result = get_bridge(THREE_BRIDGES, 1)
    >>> result == [1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, \
                  -80.275567, '1965', '2014', '2009', 4, \
                  [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    True
    """

    for items in bridge_data:
        if items[ID_INDEX] == bridge_id:
            result = items
    return result


def get_average_bci(bridge_data: List[list], bridge_id: int) -> float:
    """Return the average BCI for the bridge with bridge_id from bridge_data.
    If there is no bridge with the id bridge_id, return 0.0. If there are no
    BCIs for the bridge with id bridge_id, return 0.0.
    
    >>> get_average_bci(THREE_BRIDGES, 1)   
    70.88571428571429
    """

    for items in bridge_data:
        if items[ID_INDEX] == bridge_id:
            if items[BCIS_INDEX] == '':
                result = 0.0
            else:
                result = sum(items[BCIS_INDEX])/ len(items[BCIS_INDEX])
        else:
            result = 0.0
    return result


def get_total_length_on_highway(bridge_data: List[list], highway: str) -> float:
    """Return the total length of bridges in bridge_data on highway.
    Use zero for the length of bridges that do not have a length provided.
    If there are no bridges on highway, return 0.0.
    
    >>> get_total_length_on_highway(THREE_BRIDGES, '403')
    126.0
    >>> get_total_length_on_highway(THREE_BRIDGES, '401')
    0.0
    """

    total_length = 0.0
    for items in bridge_data:
        if items[HIGHWAY_INDEX] == highway:
            total_length = total_length + items[LENGTH_INDEX]
    return total_length


def get_distance_between(bridge1: list, bridge2: list) -> float:
    """Return the distance in kilometres, rounded to the nearest metre
    (i.e., 3 decimal places), between the two bridges bridge1 and bridge2.
        
    >>> get_distance_between(get_bridge(THREE_BRIDGES, 1), \
                                 get_bridge(THREE_BRIDGES, 2))
    1.968
    """

    return calculate_distance(bridge1[LAT_INDEX], bridge1[LON_INDEX], \
                              bridge2[LAT_INDEX], bridge2[LON_INDEX])


def find_closest_bridge(bridge_data: List[list], bridge_id: int) -> int:
    """Return the id of the bridge in bridge_data that has the shortest
    distance to the bridge with id bridge_id.
    
    Precondition: a bridge with bridge_id is in bridge_data, and there are
    at least two bridges in bridge_data
    
    >>> find_closest_bridge(THREE_BRIDGES, 2)
    1
    """

    min = float("inf")
    for items in bridge_data:
        if items[ID_INDEX] == bridge_id:
            bridge = items  

    for items in bridge_data:
        if(items[ID_INDEX] != bridge_id):
            result = get_distance_between(items, bridge)
            if result < min:
                min = result
                id = items[ID_INDEX]
    return id


def find_bridges_in_radius(bridge_data: List[list], lat: float, long: float,
                           distance: float) -> List[int]:
    """Return the IDs of the bridges that are within radius distance
    from (lat, long).
    
    >>> find_bridges_in_radius(THREE_BRIDGES, 43.10, -80.15, 50)
    [1, 2]
    """

    point = [0, 0, 0, lat, long]
    acc = []
    for items in bridge_data:
        dis = get_distance_between(point, items)
        if dis <= distance:
            acc.append(items[ID_INDEX])
    return acc


def get_bridges_with_bci_below(bridge_data: List[list], bridge_ids: List[int],
                               bci_limit: float) -> List[int]:
    """Return the IDs of the bridges with ids in bridge_ids whose most
    recent BCIs are less than or equal to bci_limit.
    
    >>> get_bridges_with_bci_below(THREE_BRIDGES, [1, 2], 72)
    [2]
    """

    acc = []
    for ids in bridge_ids:
        bridge = get_bridge(bridge_data, ids)
        if bridge[BCIS_INDEX][0] <= bci_limit:
            acc.append(bridge[ID_INDEX])
    return acc


def get_bridges_containing(bridge_data: List[list], search: str) -> List[int]:
    """
    Return a list of IDs of bridges whose names contain search (case
    insensitive).
    
    >>> get_bridges_containing(THREE_BRIDGES, 'underpass')
    [1, 2]
    >>> get_bridges_containing(THREE_BRIDGES, 'Highway')
    [1]
    """

    acc = []
    for items in bridge_data:
        if search.lower() in items[NAME_INDEX].lower():
            acc.append(items[ID_INDEX])
    return acc


def assign_inspectors(bridge_data: List[list], inspectors: List[List[float]],
                      max_bridges: int) -> List[List[int]]:
    """Return a list of bridge IDs to be assigned to each inspector in
    inspectors. inspectors is a list containing (latitude, longitude) pairs
    representing each inspector's location.
    
    At most max_bridges bridges should be assigned to an inspector, and each
    bridge should only be assigned once (to the first inspector that can
    inspect that bridge).
    
    See the "Assigning Inspectors" section of the handout for more details.
    
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 1)
    [[1]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 2)
    [[1, 2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 3)
    [[1, 2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 1)
    [[1], [2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 2)
    [[1, 2], []]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [45.0368, -81.34]],
    2)
    [[1, 2], [3]]
    >>> assign_inspectors(THREE_BRIDGES, [[38.691, -80.85], [43.20, -80.35]], 2)
    [[], [1, 2]]
    """

    (high_bci, medium_bci, low_bci, high_radius, medium_radius, low_radius) =\
        get_bci_radius(bridge_data, inspectors)
    all_ins = []
    i = 0
    for i in range(len(inspectors)):
        high1 = []
        medium1 = []
        low1 = []
        for items in bridge_data:
            if (items[ID_INDEX] in high_bci) & (items[ID_INDEX] in\
                                                high_radius[i]):
                high1.append(items[ID_INDEX])
            elif(items[ID_INDEX] in medium_bci) & (items[ID_INDEX]\
                                                    in medium_radius[i]):
                medium1.append(items[ID_INDEX])
            elif(items[ID_INDEX] in low_bci) & (items[ID_INDEX] in\
                                                              low_radius[i]):
                low1.append(items[ID_INDEX])
        high1.sort(reverse=True)
        medium1.sort(reverse=True)
        low1.sort(reverse=True)
        all_ins.append(low1 + medium1 + high1)
    return assign_now(all_ins, inspectors, max_bridges)


def assign_now(all_ins: List[List[int]], inspectors: List[List[float]],
               max_bridges: int) -> List[List[int]]:
    """
    Return the result of inspectors assignment
    >>> assign_now([[2, 1]], [[43.10, -80.15]], 1)
    [[1]]
    """

    total = []
    i = 0
    while (i < len(inspectors)):
        assign = []
        max = max_bridges
        while (len(assign) < max):
            if all_ins[i] != []:
                pop = all_ins[i].pop()
                assign += [pop]
            else:
                pop = None
                max -= 1
            check_pop(all_ins, pop, i)
        i += 1
        total.append(assign)
    return total


def check_pop(all_ins: List[List[int]], pop: int, i: int) -> None:
    """
    >>> a = [[2], [2, 1]]
    >>> check_pop(a, 1, 0)
    >>> a == [[2], [2]]
    True
    """

    if pop is not None:
        for j in all_ins[i+1:]:
            if pop in j:
                j.remove(pop)


def get_bci_radius(bridge_data: List[list], inspectors: List[List[float]]) ->\
    (List[int], List[int], List[int], List[List[int]], List[List[int]],
     List[List[int]]):
    """
    Return three lists of bcis ids and three nested lists of radius ids, from
    high to low priority.
    >>> get_bci_radius(THREE_BRIDGES, [[43.10, -80.15]])
    ([], [], [1, 2, 3], [[1, 2, 3]], [[1, 2, 3]], [[1, 2]])
    """

    ids = []
    for items in bridge_data:
        ids.append(items[ID_INDEX])
    high_bci = get_bridges_with_bci_below(bridge_data, ids, HIGH_PRIORITY_BCI)
    medium_bci = get_bridges_with_bci_below(bridge_data, ids,\
                                            MEDIUM_PRIORITY_BCI)
    low_bci = get_bridges_with_bci_below(bridge_data, ids, LOW_PRIORITY_BCI)
    high_radius = []
    medium_radius = []
    low_radius = []    
    for ins in inspectors:
        high1 = find_bridges_in_radius(bridge_data, ins[0], ins[1],
                                       HIGH_PRIORITY_RADIUS)
        medium1 = find_bridges_in_radius(bridge_data, ins[0], ins[1],
                                         MEDIUM_PRIORITY_RADIUS)
        low1 = find_bridges_in_radius(bridge_data, ins[0], ins[1],
                                      LOW_PRIORITY_RADIUS)
        high_radius.append(high1)
        medium_radius.append(medium1)
        low_radius.append(low1)
    return (high_bci, medium_bci, low_bci, high_radius, medium_radius,
            low_radius)


def inspect_bridges(bridge_data: List[list], bridge_ids: List[int], date: str, 
                    bci: float) -> None:
    """Update the bridges in bridge_data with id in bridge_ids with the new
    date and BCI score for a new inspection.
    
    >>> bridges = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,\
                  -80.275567, '1965', '2014', '2009', 4, \
                  [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                 [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                  '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61, \
                  '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3,\
                                 73.3]], \
                 [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, '1958', \
                  '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                  [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                 ]
    >>> inspect_bridges(bridges, [1], '09/15/2018', 71.9)
    >>> bridges == [[1, 'Highway 24 Underpass at Highway 403', '403', \
                     43.167233, -80.275567, '1965', '2014', '2009', 4, \
                     [12.0, 19.0, 21.0, 12.0], 65, '09/15/2018', \
                     [71.9, 72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                    [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                     '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], \
                     61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, \
                                          70.3, 73.3]], \
                    [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, \
                     '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                     [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                   ]
    True
    """
    for ids in bridge_ids:
        bridge = get_bridge(bridge_data, ids)
        bridge[LAST_INSPECTED_INDEX] = date
        bridge[BCIS_INDEX] = [bci] + bridge[BCIS_INDEX]
        bridge_data[ids - 1] = bridge


def add_rehab(bridge_data: List[list], bridge_id: int, new_date: str, 
              is_major: bool) -> None:
    """
    Update the bridge with the id bridge_id to have its last rehab set to
    new_date. If is_major is True, update the major rehab date. Otherwise,
    update the minor rehab date.
    
    >>> bridges = [[1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,\
                  -80.275567, '1965', '2014', '2009', 4, \
                  [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                  [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                 [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                  '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61, \
                  '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3,\
                                 73.3]], \
                 [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, '1958', \
                  '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                  [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                 ]
    >>> add_rehab(bridges, 1, '2018', False)
    >>> bridges == [[1, 'Highway 24 Underpass at Highway 403', '403', \
                     43.167233, -80.275567, '1965', '2014', '2018', 4, \
                     [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', \
                     [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]], \
                    [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582, \
                     '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], \
                     61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, \
                                          70.3, 73.3]], \
                    [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579, \
                     '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013', \
                     [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]] \
                   ]
    True
    """

    result = get_bridge(bridge_data, bridge_id)
    if is_major is True:
        result[LAST_MAJOR_INDEX] = new_date
    else:
        result[LAST_MINOR_INDEX] = new_date
