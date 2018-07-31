
import fire

from vert.metrics import word_movers_distance
from vert.metrics import infersent_similarity
from vert.metrics import vert_score
from vert.metrics import rouge_score
from vert.utils import vert_logger

"""
File: vert.py
Author: Jacob Krantz
Description:
    Command Line Interface for scoring the quality of sentences using VERT.
    Subscores calculated:
        Infersent Similarity (sim)
        Word Mover's Distance (wmd)
    Rouge scores can also be calculated but are not used directly in VERT.
Primary usage:
    >>> python vert.py score GENERATED TARGET [OUT_DIR]
    Full vert options:
    >>> python vert.py score
        --generated GENERATED
        --target TARGET
        [--out_dir OUT_DIR]
        [--k_value K_VALUE]
        [--rouge_type ROUGE_TYPE]
TODO: See docs for all CLI functions and arguments.
"""

def score(generated, target, out_dir='./', k_value='1/3', rouge_type=None):
    v = vert_score.Vert(k_value=k_value, rouge_type=rouge_type)
    v.load_files(generated, target)
    report = v.score()
    v.save_report_to_file(report, out_dir)
    v.display_report(report)

def wmd(generated, target, out_dir='./'):
    wm_dist = word_movers_distance.WordMoversDistance()
    wm_dist.load_files(generated, target)
    report = wm_dist.score()
    wm_dist.save_report_to_file(report, out_dir)
    wm_dist.display_report(report)

def sim(generated, target, out_dir='./'):
    i_sim = infersent_similarity.InfersentSimilarity()
    i_sim.load_files(generated, target)
    report = i_sim.score()
    i_sim.save_report_to_file(report, out_dir)
    i_sim.display_report(report)

def rouge(generated, target, rouge_type='recall', out_dir='./'):
    rg = rouge_score.Rouge(rouge_type)
    rg.load_files(generated, target)
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
