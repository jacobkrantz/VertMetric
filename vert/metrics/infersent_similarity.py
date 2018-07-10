
import logging

from vert.metrics import metric
from vert.utils import general


class InfersentSimilarity(metric.Metric):
    def __init__(self, generated, target):
        self.logger = logging.getLogger('root')
        super(InfersentSimilarity, self).__init__(generated, target)

    def score(self, make_report=True):
        self.logger.debug("Calculating Infersent Similarity scores.")
        self.logger.warn("Not implemened yet.")
        if len(self.generated) == 0:
            self.load_files()

        sim = 0.0

        self.logger.debug("Done: calculating Infersent Similarity scores.")
        if make_report:
            return self.generate_report(sim=sim)
        return sim

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
            filename = general.generate_filename('sim')
        super(InfersentSimilarity, cls).save_report_to_file(report, out_dir, filename)
