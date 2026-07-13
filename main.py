import os
from argparse import ArgumentParser
from src.hardwork import hardwork
from src.aco import TrailContribuionStrategy, PlacementStrategy
profiles = {
    'NN': {
        'rho': 1,
        'sigma': 0,
        'alpha': 0,
        'beta': 1,
        'gamma': 0,
        'lambda_': 0,
        'two_opt': False,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.SUM,
        'mmas': False,
        'mmas_smoothing': 0,
    },
    'ACO-A2B5': {
        'rho': .2,
        'sigma': 0,
        'alpha': 1,
        'beta': 5,
        'gamma': 0,
        'lambda_': 0,
        'two_opt': False,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.SUM,
        'mmas': False,
        'mmas_smoothing': 0,
    },
    # 'ACO-A2B5+2opt': {
    #     'rho': .2,
    #     'sigma': 0,
    #     'alpha': 1,
    #     'beta': 5,
    #     'gamma': 0,
    #     'lambda_': 0,
    #     'two_opt': True,
    #     'placement_strategy': PlacementStrategy.CUSTOMER,
    #     'trail_contribution_strategy': TrailContribuionStrategy.SUM,
    #     'mmas': False,
    #     'mmas_smoothing': 0,
    # },
    # 'ACO-A2B5G3L1+2opt': {
    #     'rho': .2,
    #     'sigma': 0,
    #     'alpha': 1,
    #     'beta': 5,
    #     'gamma': 3,
    #     'lambda_': 1,
    #     'two_opt': True,
    #     'placement_strategy': PlacementStrategy.CUSTOMER,
    #     'trail_contribution_strategy': TrailContribuionStrategy.SUM,
    #     'mmas': False,
    #     'mmas_smoothing': 0,
    # },
    'ACO-A1B5G3L1+2opt+MMAS+EA': {
        'rho': .2,
        'sigma': 30,
        'alpha': 1,
        'beta': 5,
        'gamma': 3,
        'lambda_': 1,
        'two_opt': True,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.BEST_IN_EPOCH,
        'mmas': True,
        'mmas_smoothing': 0,
    },
    'ACO-A1B5G2L3+2opt+MMAS+EA': {
        'rho': .2,
        'sigma': 30,
        'alpha': 1,
        'beta': 5,
        'gamma': 2,
        'lambda_': 3,
        'two_opt': True,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.BEST_IN_EPOCH,
        'mmas': True,
        'mmas_smoothing': 0,
    },

}

def main():
    cwd = os.path.abspath(os.getcwd())
    argparser = ArgumentParser()
    argparser.add_argument("output_path", help="Cartella di output")
    argparser.add_argument("--instances", help="Percorso delle istanze .vrp", default=os.path.join(cwd, 'instances'))
    argparser.add_argument("--fe", help="Numero di fitness evaluation", default=int(3.5e5), type=int)
    argparser.add_argument("--runs", help="Esecuzioni per istanza", default=5, type=int)
    argparser.add_argument("--seed", help="Seed per il generatore pseudorandom", default=0xCAFEBABE, type=int)

    #output_path = '/tmp/results' # os.path.join(cwd, 'results', 'results.csv')

    args = argparser.parse_args()
    hardwork(
        fe = args.fe,
        seed = args.seed,
        runs = args.runs,
        instances_path=args.instances,
        profiles=profiles,
        output_path=args.output_path
    )


if __name__ == "__main__":
    main()