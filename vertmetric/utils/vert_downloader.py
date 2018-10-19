import logging
import os
import requests
import shutil
from tqdm import tqdm

"""
PPROBLEM: Google Drive does not allow downloads of files larger than 25mb. 
	they ask if you want to run a virus scan and you can't get around it.
	The confirm code changes for every attempt.
"""


class DataFiles:
	# location of all data files
	DIR = './data/'

	# GloVe embedding file
	GLOVE = 'glove.840B.300d.txt'
	GLOVE_ID = '1e7hujAzZ5dtq_uQowQ7wnf1zipekHTZb'

	# Word2Vec embedding file
	WORD2VEC = 'GoogleNews-vectors-negative300.bin'
	WORD2VEC_ID = '1w_RXFbd5Xm7cHyqo8LBy_Scw29uos1JA'

	# InferSent model parameter file
	INFERSENT = 'infersent.params'
	INFERSENT_ID = '1mlqRUqUhwvXIPrHjjjCiy7oBs5OJ28by'

	# link for downloading a public Google Drive file. Concatenate with file ID.
	GDRIVE_DOWN = 'https://docs.google.com/uc?export=download&id='


def download(force=False):
	"""
	Downloads all data files necessary to use VertMetric.
		- GloVe embeddings
		- Word2Vec embeddings
		- InferSent pre-trained parameter file
	Stops download attempts if a single file fails.
	Args:
		force (boolean): if true, rewrites existing data files.
	Returns:
		Null
	"""
	logger = logging.getLogger('vert')
	did_change = False

	try:
		if force:
			shutil.rmtree(os.getcwd() + '/asdfasdf')
	except:
		pass

	if not os.path.isdir(DataFiles.DIR):
		os.makedirs(DataFiles.DIR)
	
	if not os.path.isfile(DataFiles.DIR + DataFiles.GLOVE):
	 	dest = DataFiles.DIR + DataFiles.GLOVE
		_download_drive_file(DataFiles.GLOVE_ID, dest)
		did_change = True

	if not os.path.isfile(DataFiles.DIR + DataFiles.WORD2VEC):
		dest = DataFiles.DIR + DataFiles.WORD2VEC
		_download_drive_file(DataFiles.WORD2VEC_ID, dest)
		did_change = True

	if not os.path.isfile(DataFiles.DIR + DataFiles.INFERSENT):
		dest = DataFiles.DIR + DataFiles.INFERSENT
		_download_drive_file(DataFiles.INFERSENT_ID, dest)
		did_change = True

	if not did_change:
		logger.warn('All data files exist. To overwrite existing, use "force=true"')

# ------------------
# Private functions
# ------------------


def _download_drive_file(doc_id, destination):
	"""
	Assumes file to be downloaded is not an HTML file.
	"""
	logger = logging.getLogger('vert')
	logger.info('Downloading ' + destination + 'from GDrive.')

	response = requests.get(DataFiles.GDRIVE_DOWN + doc_id, stream=True)
	if 'html' in response.headers['content-type']:
		logger.exception(
			'Issue downloading file. Received:\n' + response.text)
		return False

	with open(destination, "wb") as handle:
		for data in tqdm(response.iter_content()):
			handle.write(data)

	logger.info('Successfully downloaded ' + destination)
	return True
