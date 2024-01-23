import os
from args import get_args
from vne_simulator.base import BasicScenario
from vne_simulator import Config, REGISTRY, Generator, update_simulation_setting


def run(config):
    print(f"\n{'-' * 20}    Start     {'-' * 20}\n")
    # Load solver info: environment and solver class
    solver_info = REGISTRY.get(config.solver_name)
    Env, Solver = solver_info['env'], solver_info['solver']
    print(f'Use {config.solver_name} Solver (Type = {solver_info["type"]})...\n')

    scenario = BasicScenario.from_config(Env, Solver, config)
    scenario.run()

    print(f"\n{'-' * 20}   Complete   {'-' * 20}\n")


if __name__ == '__main__':
    # 1. Get config / Load config
    args = get_args()
    config = Config(p_net_setting_path=args.p_net_setting_path, v_sim_setting_path=args.v_sim_setting_path)
    config.update(args)
    if args.p_net_topology.lower() == 'wx100':
        config.p_net_setting['topology']['file_path'] = 'dataset/topology/Waxman100.gml'
        config.p_net_setting['num_nodes'] = 100
        config.p_net_setting_num_nodes = 100
    elif args.p_net_topology.lower() == 'geant':
        config.p_net_setting['topology']['file_path'] = 'dataset/topology/Geant.gml'
        config.p_net_setting['num_nodes'] = 40
        config.p_net_setting_num_nodes = 40
    elif args.p_net_topology.lower() == 'wx500':
        config.p_net_setting['topology']['file_path'] = 'dataset/topology/Waxman500.gml'
        config.p_net_setting['num_nodes'] = 500
        config.p_net_setting_num_nodes = 500
    else:
        raise NotImplementedError
    update_simulation_setting(
        config, 
        v_sim_setting_num_v_nets=args.v_sim_setting_num_v_nets,
        v_sim_setting_v_net_size_low=args.v_sim_setting_v_net_size_low,
        v_sim_setting_v_net_size_high=args.v_sim_setting_v_net_size_high,
        v_sim_setting_node_resource_attrs_low=args.v_sim_setting_node_resource_attrs_low,
        v_sim_setting_node_resource_attrs_high=args.v_sim_setting_node_resource_attrs_high,
        v_sim_setting_link_resource_attrs_low=args.v_sim_setting_link_resource_attrs_low,
        v_sim_setting_link_resource_attrs_high=args.v_sim_setting_link_resource_attrs_high,
        v_sim_setting_aver_arrival_rate=args.v_sim_setting_aver_arrival_rate,
        v_sim_setting_aver_lifetime=args.v_sim_setting_aver_lifetime,
    )
    # 2. Generate Dataset
    # If already generated, load from file
    p_net, v_net_simulator = Generator.generate_dataset(config, p_net=False, v_nets=False, save=False)

    # 3. Run with config
    run(config)
