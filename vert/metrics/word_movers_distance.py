
import logging

from vert.metrics import metric
from vert.utils import general


class WordMoversDistance(metric.Metric):
    def __init__(self, generated, target):
        self.logger = logging.getLogger('root')
        super(WordMoversDistance, self).__init__(generated, target)

    def score(self, make_report=True):
        self.logger.debug("Calculating Word Mover's Distance scores.")
        self.logger.warn("Not implemened yet.")
        if len(self.generated) == 0:
            self.load_files()

        wmd = 0.0

        self.logger.debug("Done: calculating Word Mover's Distance scores.")
        if make_report:
            return self.generate_report(wmd=wmd)
        return wmd

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
            filename = general.generate_filename('wmd')
        super(WordMoversDistance, cls).save_report_to_file(report, out_dir, filename)
