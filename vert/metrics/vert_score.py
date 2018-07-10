
import logging

from vert.metrics import metric
from vert.metrics import infersent_similarity
from vert.metrics import word_movers_distance
from vert.metrics import rouge

from vert.utils import general


class Vert(metric.Metric):
    def __init__(self, generated_f, target_f, include_rouge, k_value):
        self.logger = logging.getLogger('root')
        super(Vert, self).__init__(generated_f, target_f)

        self.include_rouge = include_rouge
        self.k_value = k_value
        self.wmd = word_movers_distance.WordMoversDistance
        self.sim = infersent_similarity.InfersentSimilarity
        self.rouge = rouge.Rouge

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
        if len(self.generated) == 0:
            self.load_files()

        wmd_score = 0.0
        sim_score = 0.0
        vert_score = 0.0
        if self.include_rouge:
            rouge_1 = 0.0
            rouge_2 = 0.0
            rouge_l = 0.0

        self.logger.debug("Done: calculating VERT scores.")
        if make_report:
            if self.include_rouge:
                return self.generate_report(
                    rouge_1=rouge_1,
                    rouge_2=rouge_2,
                    rouge_l=rouge_l,
                    wmd=wmd_score,
                    sim=sim_score,
                    vert=vert_score
                )
            return self.generate_report(
                wmd=wmd_score,
                sim=sim_score,
                vert=vert_score
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
            filename = general.generate_filename('vert')
        super(Vert, cls).save_report_to_file(report, out_dir, filename)
