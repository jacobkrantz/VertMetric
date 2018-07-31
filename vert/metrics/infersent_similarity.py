
import logging
from sklearn.metrics.pairwise import cosine_similarity
import torch

from vert.metrics import metric
from vert.utils import general as gen


class InfersentSimilarity(metric.Metric):
    def __init__(self):
        self.logger = logging.getLogger('root')
        super(InfersentSimilarity, self).__init__()

    def score(self, make_report=True):
        self.logger.debug("Calculating Infersent Similarity scores.")
        self.logger.warn("Not implemened yet.")
        gen.check_data_loaded(self.generated, self.targets)

        infersent = torch.load(
            "./data/infersent.allnli.pickle",
            map_location=lambda storage,
            loc: storage
        )
        infersent.set_glove_path("./data/glove.840B.300d.txt")
        infersent.build_vocab_k_words(1000000)

        embeddings_1 = infersent.encode(self.generated, tokenize=True)
        self.logger.debug('InferSent: Embeddings generated for group 1.')
        embeddings_2 = infersent.encode(self.targets, tokenize=True)
        self.logger.debug('InferSent: Embeddings generated for group 2.')

        sim = np.mean(list(starmap(
            lambda e1,e2: self._cos_sim(e1,e2),
            zip(embeddings_1, embeddings_2)
        )))

        self.logger.debug("Done: calculating Infersent Similarity scores.")
        if make_report:
            return self.generate_report(sim=gen.fmt_rpt_line(sim))
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
            filename = gen.generate_filename('sim')
        super(InfersentSimilarity, cls).save_report_to_file(report, out_dir, filename)

    def _cos_sim(self, sentence_1, sentence_2):
        """
        Only call with one sentence at a time.
        """
        return cosine_similarity(
            sentence_1.reshape(1,-1),
            sentence_2.reshape(1,-1)
        )[0][0]
