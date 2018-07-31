
import logging
import numpy as np

from vert.metrics import metric
from vert.metrics import infersent_similarity
from vert.metrics import word_movers_distance
from vert.metrics import rouge_score
from vert.utils import general as gen


class Vert(metric.Metric):
    def __init__(self, alpha=5, rouge_type=None):
        self.logger = logging.getLogger('root')
        super(Vert, self).__init__()

        self.rouge_type = rouge_type
        self.alpha = float(alpha)
        self.wmd = word_movers_distance.WordMoversDistance
        self.sim = infersent_similarity.InfersentSimilarity
        self.rouge = rouge_score.Rouge

    def score(self, make_report=True):
        """
        Calculates the VERT score for the generated summaries as compared to
            the respective targets.
        Args:
            make_report (bool): if True, returns a score report containing each
                sub-score. Otherwise returns the individual VERT score.
        Returns:
            dict: score report
            OR
            float: vert score
        """
        self.logger.debug("Calculating VERT scores.")
        gen.check_data_loaded(self.generated, self.targets)

        # Calculate Infersent cosine similarity
        self.sim = self.sim()
        self.sim.set_generated_and_targets(self.generated, self.targets)
        sim_score = self.sim.score(make_report=False)
        del self.sim

        # Calcuate word mover's distance
        self.wmd = self.wmd()
        self.wmd.set_generated_and_targets(self.generated, self.targets)
        wmd_score = self.wmd.score(make_report=False)
        del self.wmd

        # Calculate VERT score
        vert_score = self._calc_vert_final(sim_score, wmd_score)

        # Calculate all ROUGE scores
        if self.rouge_type is not None:
            self.rouge = self.rouge(type=self.rouge_type)
            self.rouge.set_generated_and_targets(self.generated, self.targets)
            r_scores = self.rouge.score(make_report=False)
            rouge_1 = r_scores['rouge_1']
            rouge_2 = r_scores['rouge_2']
            rouge_l = r_scores['rouge_l']
            rouge_type = r_scores['rouge_type']
            del self.rouge

        self.logger.debug("Done: calculating VERT scores.")
        if make_report:
            if self.rouge_type is not None:
                return self.generate_report(
                    rouge_1=gen.fmt_rpt_line(rouge_1),
                    rouge_2=gen.fmt_rpt_line(rouge_2),
                    rouge_l=gen.fmt_rpt_line(rouge_l),
                    rouge_type=rouge_type,
                    wmd=gen.fmt_rpt_line(wmd_score),
                    sim=gen.fmt_rpt_line(sim_score),
                    vert=gen.fmt_rpt_line(vert_score)
                )
            return self.generate_report(
                wmd=gen.fmt_rpt_line(wmd_score),
                sim=gen.fmt_rpt_line(sim_score),
                vert=gen.fmt_rpt_line(vert_score)
            )
        return vert_score

    @classmethod
    def save_report_to_file(cls, report, out_dir='./', filename=''):
        """
        Args:
            report (dict): metrics calculated to be dumped to JSON
            filename (str): optional specification.
        Returns:
            None
        """
        if filename == '':
            filename = gen.generate_filename('vert')
        super(Vert, cls).save_report_to_file(report, out_dir, filename)

    def _calc_vert_final(self, sim, dis):
        return (1./2.) * (1. + (sim - ((1./self.alpha) * dis)))
