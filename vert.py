
import fire

from vert.metrics import word_movers_distance
from vert.metrics import infersent_similarity
from vert.metrics import vert_score
from vert.metrics import rouge as rge

from vert.utils import vert_logger
"""
File: vert.py
Author: Jacob Krantz
Description:
    Command Line Interface for scoring the quality of sentences using VERT.
    Subscores calculated:
        Infersent Similarity (sim)
        Word Mover's Distance (wmd)
    Rouge scores can also be calculated but are not used in VERT.
Primary usage:
    >>> python vert.py score GENERATED TARGET [OUT_DIR] [INCLUDE_ROUGE]
    Full options:
    >>> python vert.py score
        --generated GENERATED
        --target TARGET
        [--out-dir OUT_DIR]
        [--include-rouge INCLUDE_ROUGE]
        [--k_value K_VALUE]
"""

def score(generated, target, out_dir='./', include_rouge=False, k_value=3):
    v = vert_score.Vert(generated, target, include_rouge, k_value)
    report = v.score()
    v.save_report_to_file(report, out_dir)
    v.display_report(report)

def wmd(generated, target, out_dir='./'):
    wm_dist = word_movers_distance.WordMoversDistance(generated, target)
    report = wm_dist.score()
    wm_dist.save_report_to_file(report, out_dir)
    wm_dist.display_report(report)

def sim(generated, target, out_dir='./'):
    i_sim = infersent_similarity.InfersentSimilarity(generated, target)
    report = i_sim.score()
    i_sim.save_report_to_file(report, out_dir)
    i_sim.display_report(report)

def rouge(generated, target, out_dir='./'):
    rg = rge.Rouge(generated, target)
    report = rg.score()
    rg.save_report_to_file(report, out_dir)
    rg.display_report(report)

if __name__ == '__main__':
    vert_logger.setup_custom_logger('root')
    fire.Fire({
        'score': score,
        'wmd': wmd,
        'sim': sim,
        'rouge': rouge,
    })
