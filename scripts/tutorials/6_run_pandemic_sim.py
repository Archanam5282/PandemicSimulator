# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.
from tqdm import trange

import pandemic_simulator as ps


def run_pandemic_sim() -> None:
    """Here we execute the simulator using austin regulations, a small town config and default person routines."""

    print('\nA tutorial that runs the simulator using austin regulations and default person routines', flush=True)

    # init globals
    ps.init_globals(seed=0)

    # select a simulator config
    sim_config = ps.sh.small_town_config

    # make sim
    sim = ps.env.PandemicSim.from_config(sim_config, person_routine_assignment=ps.sh.DefaultPersonRoutineAssignment())

    # setup viz to show plots
    viz = ps.viz.MatplotLibViz(num_persons=sim_config.num_persons,
                               max_hospital_capacity=sim_config.max_hospital_capacity,
                               num_stages=len(ps.sh.austin_regulations),
                               show_stages=False)

    # impose a regulation
    sim.impose_regulation(regulation=ps.sh.austin_regulations[0])  # stage 0

    # run regulation steps in the simulator
    for _ in trange(100, desc='Simulating day'):
        sim.step_day()
        viz.record(sim.state)

    # generate plots
    viz.plot()


if __name__ == '__main__':
    run_pandemic_sim()
