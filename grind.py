import os
from argparse import ArgumentParser
from src.grinder import grinder
from src.aco import TrailContribuionStrategy, PlacementStrategy
profiles = {
    'NN': {
        'rho': 0,
        'alpha': 0,
        'beta': 1,
        'gamma': 0,
        'lambda_': 0,
        'sigma': 0,
        'two_opt': False,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.SUM,
        'mmas': False,
        'mmas_smoothing': 0,
    },
    'AS': {
        'rho': .25,
        'alpha': 1,
        'beta': 5,
        'gamma': 0,
        'lambda_': 0,
        'sigma': 'auto',
        'two_opt': False,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.SUM,
        'mmas': True,
        'mmas_smoothing': 0,
    },  
    'HAS': {
        'rho': .25,
        'alpha': 1,
        'beta': 5,
        'gamma': 0,
        'lambda_': 0,
        'sigma': 'auto',
        'two_opt': True,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.SUM,
        'mmas': True,
        'mmas_smoothing': 0,
    },
    'HAS-SAV': {
        'rho': .25,
        'alpha': 1,
        'beta': 5,
        'gamma': 5,
        'lambda_': 0,
        'sigma': 'auto',
        'two_opt': True,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.SUM,
        'mmas': True,
        'mmas_smoothing': 0,
    },
    'HAS-CAP': {
        'rho': .25,
        'alpha': 1,
        'beta': 5,
        'gamma': 0,
        'lambda_': 5,
        'sigma': 'auto',
        'two_opt': True,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.SUM,
        'mmas': True,
        'mmas_smoothing': 0,
    },
    'HAS-1': {
        'rho': .25,
        'alpha': 1,
        'beta': 5,
        'gamma': 5,
        'lambda_': 5,
        'sigma': 'auto',
        'two_opt': True,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.SUM,
        'mmas': True,
        'mmas_smoothing': 0,
    },
    'HAS-5': {
        'rho': .25,
        'alpha': 5,
        'beta': 5,
        'gamma': 5,
        'lambda_': 5,
        'sigma': 'auto',
        'two_opt': True,
        'placement_strategy': PlacementStrategy.CUSTOMER,
        'trail_contribution_strategy': TrailContribuionStrategy.SUM,
        'mmas': True,
        'mmas_smoothing': 0,
    },
    

}

def main():
    cwd = os.path.abspath(os.getcwd())
    argparser = ArgumentParser()
    argparser.add_argument("output", help="File di output (.csv)")
    argparser.add_argument("--instances", help="Percorso delle istanze .vrp", default=os.path.join(cwd, 'instances'))
    argparser.add_argument("--fe", help="Numero di fitness evaluation", default=int(3.5e5), type=int)
    argparser.add_argument("--runs", help="Esecuzioni per istanza", default=5, type=int)
    argparser.add_argument("--seed", help="Seed per il generatore pseudorandom", default=0xCAFEBABE, type=int)

    #output_path = '/tmp/results' # os.path.join(cwd, 'results', 'results.csv')

    args = argparser.parse_args()
    grinder(
        fe = args.fe,
        seed = args.seed,
        runs = args.runs,
        instances_path=args.instances,
        profiles=profiles,
        output_file=args.output
    )


if __name__ == "__main__":
    main()