import inspect

import sklearn
from sklearn.utils.estimator_checks import check_estimator

import skmine.itemsets
# TODO : add other modules here

MODULES = [
    skmine.itemsets,
]

OK = '\x1b[42m[ OK ]\x1b[0m'
FAIL = "\x1b[41m[FAIL]\x1b[0m"

def is_estimator(e):
    _, est = e
    meth = getattr(est, "fit", None)
    return callable(meth)

if __name__ == '__main__':
    for module in MODULES:
        clsmemembers = inspect.getmembers(skmine.itemsets, inspect.isclass)
        estimators = filter(is_estimator, clsmemembers)
        for est_name, est in estimators:
            # from sklearn 0.23 check_estimator takes an instance as input
            obj = est() if sklearn.__version__[:4] >= '0.23' else est
            checks = check_estimator(obj, generate_only=True)
            for arg, check in checks:
                check_name = check.func.__name__  # unwrap partial function
                desc = '{} === {}'.format(est_name, check_name)
                try:
                    check(arg)
                    print(OK, desc)
                except Exception as e:
                    print(FAIL, desc, e)
