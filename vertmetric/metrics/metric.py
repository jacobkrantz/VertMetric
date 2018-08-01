
import json
import logging
import os

from vertmetric.utils import general as gen

"""
Base class for all metrics used in the vert evaluation.
All subclasses must override the score() function.
Any of the below functions can be overridden.
"""

class Metric(object):
    def __init__(self):
        self.generated = list()
        self.targets = list()

    def score(self, make_report=True):
        raise NotImplementedError("Subclasses of Metric must implement this.")

    def load_files(self, generated_f, target_f):
        """
        Loads self.generated and self.targets with summaries from their
            respective files.
        Args:
            generated_f (str): filename of the generated summaries. Each line
                is its own summary.
            target_f (str): target filename. Contains target summaries for
                the generated summaries to be compared to. Each line is its
                own summary. line[i] of target_f corresponds to line[i] of
                the generated_f.
        Returns:
            None
        """
        self.generated = list()
        self.targets = list()

        with open(generated_f, 'r') as gen_f:
            for line in gen_f:
                line = line.strip('\n')
                self.generated.append(line)

        with open(target_f, 'r') as tgt_f:
            for line in tgt_f:
                line = line.strip('\n')
                self.targets.append(line)
        gen.verify_data(self.generated, self.targets)

    def set_generated_and_targets(self, generated, targets):
        """
            Can set self.generated and self.targets manually.
            Args:
                generated (list<str>): list of generated summaries. Loads into
                    self.generated.
                targets (list<str>): list of target summaries. Loads into
                    self.targets.
            Returns:
                None
        """
        self.targets = targets
        self.generated = generated
        gen.verify_data(self.generated, self.targets)

    def generate_report(self, **kwargs):
        report = {
            'num_tested':str(len(self.generated)),
            'avg_generated_word_cnt':gen.fmt_rpt_line(gen.avg_word_count(self.generated)),
            'avg_target_word_cnt':gen.fmt_rpt_line(gen.avg_word_count(self.targets)),
        }
        for key, value in kwargs.iteritems():
            report[key] = value
        return report

    @classmethod
    def display_report(cls, report):
        print('-------------------------------')
        print('         score report          ')
        print('-------------------------------')
        for k, v in report.iteritems():
            if len(k) >= 15:
                tab = ':\t'
            elif len(k) < 5:
                tab = tab = ':\t\t\t'
            else:
                tab = ':\t\t'
            print(k + tab + str(v))

    @classmethod
    def save_report_to_file(cls, report, out_dir, filename):
        """
        Dumps a score report dictionary as JSON to a specified file.
        Args:
            report (dict):
            out_dir (string): directory to save report.
            filename (string): location to save report.
        """
        logger = logging.getLogger('root')
        if type(report) != dict:
            logger.exception('Report needs to be a python dict.')
            raise ValueError('Report needs to be a python dict.')
        if not len(report):
            logger.warning('Saving empty report.')

        out_dir = out_dir + '/' if out_dir[-1] != '/' else out_dir
        if os.path.isfile(out_dir + filename):
            logger.info('Overwriting existing file.')

        with open(out_dir + filename, 'w') as f:
            json.dump(report, f, indent=2, sort_keys=True)
        logger.info('Saved report to \'' + out_dir + filename + '\'')
