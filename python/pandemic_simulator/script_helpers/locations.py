# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.

from typing import List, Optional

import numpy as np

from ..environment import Home, Location, CityRegistry, GroceryStore, Road, Cemetery, Hospital, \
    Office, School, Restaurant, SimTimeTuple, HospitalState, ContactRate, BusinessLocationState, \
    NonEssentialBusinessLocationState, RetailStore, HairSalon, PopulationParams, Bar, LocationID

__all__ = ['make_standard_locations']


def make_standard_locations(population_params: PopulationParams,
                            registry: CityRegistry,
                            numpy_rng: Optional[np.random.RandomState] = None) -> List[Location]:
    numpy_rng = numpy_rng if numpy_rng is not None else np.random.RandomState()
    location_type_to_params = population_params.location_type_to_params
    req_loc_types = [Hospital, Home, GroceryStore, Office, School]
    for loc_type in req_loc_types:
        assert loc_type in location_type_to_params, f'loc_type - {loc_type} is required for this helper.'

    road = Road(registry, loc_id=LocationID('road'), numpy_rng=numpy_rng)

    cemetery = Cemetery(registry, loc_id=LocationID('cemetery'), road_id=road.id, numpy_rng=numpy_rng)

    hospitals: List[Location] = [Hospital(registry=registry,
                                          loc_id=LocationID(f'hospital_{i}', ('Hospital',)),
                                          road_id=road.id,
                                          init_state=HospitalState(
                                              is_open=True,
                                              contact_rate=ContactRate(0, 3, 1, 0.1, 0., 0.),
                                              visitor_capacity=location_type_to_params[Hospital].visitor_capacity,
                                              patient_capacity=location_type_to_params[Hospital].visitor_capacity),
                                          numpy_rng=numpy_rng
                                          ) for i in range(location_type_to_params[Hospital].num)]

    homes: List[Location] = [Home(registry=registry,
                                  loc_id=LocationID(f'home_{i}', ('Home',)),
                                  road_id=road.id,
                                  numpy_rng=numpy_rng)
                             for i in range(location_type_to_params[Home].num)]

    grocery_stores: List[Location] = [GroceryStore(
        registry=registry,
        loc_id=LocationID(f'grocery_{i}', ('GroceryStore',)),
        road_id=road.id,
        init_state=BusinessLocationState(
            is_open=True,
            contact_rate=ContactRate(0, 1, 0, 0.2, 0.25, 0.3),
            visitor_capacity=location_type_to_params[GroceryStore].visitor_capacity,
            open_time=SimTimeTuple(hours=tuple(range(7, 21)), week_days=tuple(range(0, 6)))),
        numpy_rng=numpy_rng
    ) for i in range(location_type_to_params[GroceryStore].num)]

    offices: List[Location] = [Office(
        registry=registry,
        loc_id=LocationID(f'offices_{i}', ('Office',)),
        road_id=road.id,
        init_state=NonEssentialBusinessLocationState(
            is_open=True,
            contact_rate=ContactRate(2, 1, 0, 0.1, 0.01, 0.01),
            visitor_capacity=location_type_to_params[Office].visitor_capacity,
            open_time=SimTimeTuple(hours=tuple(range(9, 17)), week_days=tuple(range(0, 5)))),
        numpy_rng=numpy_rng
    ) for i in range(location_type_to_params[Office].num)]

    schools: List[Location] = [School(
        registry=registry,
        loc_id=LocationID(f'school_{i}', ('School',)),
        road_id=road.id,
        init_state=NonEssentialBusinessLocationState(
            is_open=True,
            contact_rate=ContactRate(5, 1, 0, 0.1, 0., 0.1),
            visitor_capacity=location_type_to_params[School].visitor_capacity,
            open_time=SimTimeTuple(hours=tuple(range(7, 15)), week_days=tuple(range(0, 5)))),
        numpy_rng=numpy_rng
    ) for i in range(location_type_to_params[School].num)]

    all_locs: List[Location] = homes + grocery_stores + offices + schools + hospitals + [road, cemetery]

    if RetailStore in location_type_to_params:
        all_locs += [RetailStore(
            registry=registry,
            loc_id=LocationID(f'retail_{i}', ('RetailStore',)),
            road_id=road.id,
            init_state=NonEssentialBusinessLocationState(
                is_open=True,
                contact_rate=ContactRate(0, 1, 0, 0.2, 0.25, 0.3),
                visitor_capacity=location_type_to_params[RetailStore].visitor_capacity,
                open_time=SimTimeTuple(hours=tuple(range(7, 21)), week_days=tuple(range(0, 6)))),
            numpy_rng=numpy_rng
        ) for i in range(location_type_to_params[RetailStore].num)]

    if HairSalon in location_type_to_params:
        all_locs += [HairSalon(
            registry=registry,
            loc_id=LocationID(f'hair_salon_{i}', ('HairSalon',)),
            road_id=road.id,
            init_state=NonEssentialBusinessLocationState(
                is_open=True,
                contact_rate=ContactRate(1, 1, 0, 0.5, 0.3, 0.1),
                visitor_capacity=location_type_to_params[HairSalon].visitor_capacity,
                open_time=SimTimeTuple(hours=tuple(range(9, 17)), week_days=tuple(range(1, 7)))),
            numpy_rng=numpy_rng
        ) for i in range(location_type_to_params[HairSalon].num)]

    if Bar in location_type_to_params:
        all_locs += [Bar(
            registry=registry,
            loc_id=LocationID(f'bar_{i}', ('Bar',)),
            road_id=road.id,
            init_state=NonEssentialBusinessLocationState(
                is_open=True,
                contact_rate=ContactRate(1, 1, 0, 0.7, 0.2, 0.1),
                visitor_capacity=location_type_to_params[Bar].visitor_capacity,
                open_time=SimTimeTuple(hours=tuple(range(21, 24)),
                                       week_days=tuple(range(1, 7)))),
            numpy_rng=numpy_rng
        ) for i in range(location_type_to_params[Bar].num)]

    if Restaurant in location_type_to_params:
        all_locs += [Restaurant(
            registry=registry,
            loc_id=LocationID(f'restaurant_{i}', ('Restaurant',)),
            road_id=road.id,
            init_state=NonEssentialBusinessLocationState(
                is_open=True,
                contact_rate=ContactRate(1, 1, 0, 0.3, 0.35, 0.1),
                visitor_capacity=location_type_to_params[Restaurant].visitor_capacity,
                open_time=SimTimeTuple(hours=tuple(range(11, 16)) + tuple(range(19, 24)),
                                       week_days=tuple(range(1, 7)))),
            numpy_rng=numpy_rng
        ) for i in range(location_type_to_params[Restaurant].num)]

    return all_locs
