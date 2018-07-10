
import logging

from vert.metrics import metric
from vert.utils import general


class Rouge(metric.Metric):
    def __init__(self, generated, target):
        self.logger = logging.getLogger('root')
        super(Rouge, self).__init__(generated, target)

    def score(self, make_report=True):
        self.logger.debug("Calculating ROUGE scores.")
        self.logger.warn("Not implemened yet.")
        if len(self.generated) == 0:
            self.load_files()

        rouge_1 = 0.0
        rouge_l = 0.0
        rouge_2 = 0.0

        self.logger.debug("Done: calculating ROUGE scores.")
        if make_report:
            return self.generate_report(
                rouge_1=rouge_1,
                rouge_2=rouge_2,
                rouge_l=rouge_l
            )
        return {'rouge_1':rouge_1,'rouge_2':rouge_2,'rouge_l':rouge_l}

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
            filename = general.generate_filename('rouge')
        super(Rouge, cls).save_report_to_file(report, out_dir, filename)
