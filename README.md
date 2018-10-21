# VertMetric
The Versatile Evaluation of Reduced Texts metric (VERT) is an abstractive summarization evaluation package. Abstractive summaries allow for a summary to include words that are different than the specfic ones included in the original text. This is unlike the more traditional approach of extractive summarization, where words are selected from the original text and reordered. Existing evaluation metrics fail to accurately judge modern abstractive summaries. VERT exists to fill this hole.

## What does VertMetric do?  
VertMetric evaluates the VERT score for a collection of generated summaries. VertMetric can also be used to calculate ROUGE scores (ROUGE-1, ROUGE-2, ROUGE-L) and generate a score report with all these elements. VERT has only been used for sentence summaries so far, but that doesn't mean it cannot be used for longer one. I would appreciate hearing how VERT does in evaluating longer summaries!    

## Preparation Instructions  

#### Requirements:  
- 9GB free disc space  
- 10+ GB RAM  
- Python 2.7  

#### Steps:  

1. Clone this repository:  
```
$ git clone https://github.com/jacobkrantz/VertMetric.git
```  
2. Install Python 2.7 dependencies:  
```
$ pip install -r requirements.txt
```  
There is a chance this will fail while installing `pyemd`. If the error contains a reference to `Python.h`, you need to install `python-dev` first:  
```
$ sudo apt-get install python-dev
```
3. Download necessary data files (3) and move them into the `/data` folder:  
- GloVe file: https://drive.google.com/file/d/1e7hujAzZ5dtq_uQowQ7wnf1zipekHTZb/view?usp=sharing  
- Word2Vec file: https://drive.google.com/file/d/1w_RXFbd5Xm7cHyqo8LBy_Scw29uos1JA/view?usp=sharing  
- InferSent params file: https://drive.google.com/file/d/1mlqRUqUhwvXIPrHjjjCiy7oBs5OJ28by/view?usp=sharing  

You should now be ready to try out the metric!  

## General Use Instructions  
We evaluate summaries by comparing them to a gold standard summary, not the original text. For sentence summarization, the dataset of DUC2004 serves as the standard example. The steps outlined below are for a normal use of this software (generate both VERT and ROUGE scores).  

#### Steps:  

1. Create a text file containing one generated summary per line. Example: `./generated.txt`.
2. Create another text file containing one target summary per line. Example: `./targets.txt`.
3. Ensure a directory exists to store report outputs. Example: `./reports`.
3. Run the evaluation. This creates a JSON file with the results. 
```
python vert.py score \
  --generated='./generated.txt' \
  --target='./targets.txt' \
  --out_dir='./reports' \
  --rouge_type recall
```
The above run command calculates the average VERT and ROUGE scores for all summaries in `generated.txt` using a line-by-line comparison with `targets.txt`. The score report is stored in `./reports`.  

You may find it easier to make changes to and use `./run.sh` instead of typing the whole command each time. 

#### Understanding Score Reports  
Example score report:
```
{
  "avg_generated_word_cnt": "5.500", 
  "avg_target_word_cnt": "4.500", 
  "num_tested": "2", 
  "rouge_1": "50.000", 
  "rouge_2": "25.000", 
  "rouge_l": "50.000", 
  "rouge_type": "recall", 
  "sim": "0.661", 
  "wmd": "2.412", 
  "vert": "0.589"
}
```
- avg_generated_word_cnt: the average character length of the -generated summaries.  
- avg_target_word_cnt: the average character length of the target summaries.  
- num_tested: the number of summaries included in the evaluation.  
- rouge_1: standard ROUGE-1 score. ROUGE scores calculated using the [rouge](https://github.com/pltrdy/rouge) library.  
- rouge_2: standard ROUGE-2 score.  
- rouge_l: standard ROUGE-L score.  
- sim: InferSent cosine similarity (similarity sub-score of VERT).  
- wmd: word mover's distance (dissimilarity sub-score of VERT).
- vert: average overall VERT score of the generated summaries.  

VERT ranges from 0->1, with 1 being an identical summary. 

## Acknowledgements
If this code helps you with your research, please consider citing our paper where these ideas came from.  
*paste bibtex and arxiv link here*

This code is developed in part with support from the National Science Foundation under Grant No. 1659788 at the University of Colorado, Colorado Springs.

## TODO  
- installation with setup.py currently does not work. 
- It would be nice to have a download script for the above data files. I don't think Google Drive allows this because of the file size, but this would be really nice to figure out.  
- optimize the code to have lower memory requirements.
