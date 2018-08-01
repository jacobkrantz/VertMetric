
import logging
from rouge import Rouge as RougeLib

from vertmetric.metrics import metric
from vertmetric.utils import general as gen


class Rouge(metric.Metric):
    def __init__(self, type='recall'):
        """
        Subclass of Metric.
        Args:
            type (str): ('recall'|'precision'|'f-measure')
        """
        super(Rouge, self).__init__()
        self.logger = logging.getLogger('vert')
        if type not in ['recall','precision','f-measure']:
            msg = "Type must be one of 'recall','precision', or 'f-measure'."
            self.logger.exception(msg)
            raise ValueError(msg)
        self.type = type

    def score(self, full_report=True):
        self.logger.info("Calculating ROUGE scores.")

        gen.check_data_loaded(self.generated, self.targets)
        r_scores = RougeLib().get_scores(
            self.generated,
            self.targets,
            avg=True
        )
        rouge_1 = r_scores['rouge-1'][self.type[0]] * 100
        rouge_2 = r_scores['rouge-2'][self.type[0]] * 100
        rouge_l = r_scores['rouge-l'][self.type[0]] * 100

        self.logger.info("Done: calculating ROUGE scores.")
        if full_report:
            return self.generate_report(
                rouge_1=gen.fmt_rpt_line(rouge_1),
                rouge_2=gen.fmt_rpt_line(rouge_2),
                rouge_l=gen.fmt_rpt_line(rouge_l),
                rouge_type=self.type
            )
        return {
            'rouge_1':gen.fmt_rpt_line(rouge_1),
            'rouge_2':gen.fmt_rpt_line(rouge_2),
            'rouge_l':gen.fmt_rpt_line(rouge_l),
            'rouge_type':self.type
        }

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
            filename = gen.generate_filename('rouge')
        super(Rouge, cls).save_report_to_file(report, out_dir, filename)
