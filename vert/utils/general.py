
from datetime import datetime
import numpy as np

def tokenize(txt):
    return txt.strip('\n')

def generate_filename(scope):
    time = datetime.now().strftime('%B-%d_%H:%M:%S_')
    return time + scope + '-score-report.json'

def avg_word_count(lst):
    """
    Computes the average word count of each list element by splitting
        on whitespace.
    Returns:
        float
    """
    return float(np.mean(list(map(lambda s: len(s.split()), lst))))

def verify_data(generated, targets):
    """
    Throws an error if the generated and/or targets lists are
        incorrect for comparison.
    Returns:
        None
    """
    try:
        assert len(generated) == len(targets)
    except AssertionError as err:
        logger = logging.getLogger('root')
        logger.exception("Unequal number of summaries in generated vs target files.")
        raise err

    try:
        assert len(generated) > 0
    except AssertionError as err:
        logger = logging.getLogger('root')
        logger.exception("0 summaries being compared.")
        raise err
