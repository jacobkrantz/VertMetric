
from gensim.models import KeyedVectors
from itertools import starmap
import logging
from nltk.corpus import stopwords
from nltk.downloader import Downloader
from nltk import download
import numpy as np

from vertmetric.metrics import metric
from vertmetric.utils import general as gen


class WordMoversDistance(metric.Metric):
    def __init__(self):
        self.logger = logging.getLogger('vert')
        super(WordMoversDistance, self).__init__()

        self.logger.info("Loading Word2Vec embeddings.")
        if not Downloader().is_installed('stopwords'):
            download('stopwords')
        self.stopwords = stopwords.words('english')
        self.model = KeyedVectors.load_word2vec_format(
            "./data/GoogleNews-vectors-negative300.bin", #.gz takes 2.5x longer
            binary=True
        )
        self.logger.info("Done: loading Word2Vec embeddings.")

    def score(self, make_report=True):
        self.logger.info("Calculating Word Mover's Distance scores.")
        gen.check_data_loaded(self.generated, self.targets)

        wmd = np.mean(list(starmap(
            lambda s1,s2: self.get_single_wmd(s1,s2),
            zip(self.generated, self.targets)
        )))

        self.logger.info("Done: calculating Word Mover's Distance scores.")
        if make_report:
            return self.generate_report(wmd=gen.fmt_rpt_line(wmd))
        return wmd

    def get_single_wmd(self, sentence_1, sentence_2):
        """
        Calculates the word mover's distance for a single sentence pair.
        If the distance is greater than 5.0, truncates to 5.0. This is because
        model.wmdistance() occasionally returns 'inf'.
        Returns:
            float: WMD with a range of [0.0,5.0]
        """
        sentence_1 = sentence_1.lower().split()
        sentence_2 = sentence_2.lower().split()

        sentence_1 = [w for w in sentence_1 if w not in self.stopwords]
        sentence_2 = [w for w in sentence_2 if w not in self.stopwords]

        max_dist = 5.0
        dist = self.model.wmdistance(sentence_1, sentence_2)
        return dist if dist < max_dist else max_dist

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
            filename = gen.generate_filename('wmd')
        super(WordMoversDistance, cls).save_report_to_file(report, out_dir, filename)
