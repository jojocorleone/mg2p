#!/usr/bin/env python

"""
Functions for measuring and visualizing the performance of g2p models.

todo: functions for comparing one model's results to another's
"""

from os.path import join
import pandas as pd
import numpy as np

HIGH_RESOURCE = ['ady', 'afr', 'ain', 'amh', 'ang', 'ara', 'arc', 'ast', 
                'aze', 'bak', 'ben', 'bre', 'bul', 'cat', 'ces', 'cym', 
                'dan', 'deu', 'dsb', 'ell', 'eng', 'epo', 'eus', 'fao', 
                'fas', 'fin', 'fra', 'gla', 'gle', 'hbs', 'heb', 'hin', 
                'hun', 'hye', 'ido', 'isl', 'ita', 'jbo', 'jpn', 'kat', 
                'kbd', 'kor', 'kur', 'lao', 'lat', 'lav', 'lit', 'ltz', 
                'mkd', 'mlt', 'msa', 'mya', 'nan', 'nci', 'nld', 'nno', 
                'nob', 'oci', 'pol', 'por', 'pus', 'ron', 'rus', 'san', 
                'scn', 'sco', 'sga', 'slk', 'slv', 'spa', 'sqi', 'swe', 
                'syc', 'tel', 'tgk', 'tgl', 'tha', 'tur', 'ukr', 'urd', 
                'vie', 'vol', 'yid', 'yue', 'zho']
                
LOW_RESOURCE = ['aar', 'abk', 'abq', 'ace', 'ach', 'agr', 'aka', 'akl', 
                'akz', 'ale', 'alt', 'ami', 'aqc', 'arg', 'arw', 'arz', 
                'asm', 'ava', 'aym', 'bal', 'bam', 'bcl', 'bel', 'bis', 
                'bod', 'bos', 'bua', 'bug', 'ceb', 'cha', 'che', 'chk', 
                'chm', 'cho', 'chv', 'cic', 'cjs', 'cor', 'crh', 'dar', 
                'est', 'ewe', 'fij', 'fil', 'frr', 'fry', 'fur', 'gaa', 
                'gag', 'glg', 'grc', 'grn', 'gsw', 'guj', 'hak', 'hat', 
                'hau', 'haw', 'hil', 'hit', 'hrv', 'iba', 'ilo', 'ind', 
                'inh', 'jam', 'jav', 'kaa', 'kab', 'kal', 'kan', 'kaz', 
                'kea', 'ket', 'khb', 'kin', 'kir', 'kjh', 'kom', 'kum', 
                'lin', 'lld', 'lug', 'luo', 'lus', 'lzz', 'mah', 'mal', 
                'mar', 'mlg', 'mnk', 'mns', 'moh', 'mon', 'mri', 'mus', 
                'mww', 'myv', 'mzn', 'nah', 'nap', 'nau', 'nds', 'nep', 
                'new', 'nia', 'niu', 'non', 'nor', 'nso', 'oss', 'osx', 
                'pag', 'pam', 'pan', 'pau', 'pon', 'ppl', 'prs', 'que', 
                'roh', 'rom', 'rtm', 'ryu', 'sac', 'sah', 'sat', 'sei', 
                'sme', 'sna', 'snd', 'som', 'sot', 'srd', 'srp', 'sun', 
                'swa', 'tam', 'tat', 'tay', 'tir', 'tkl', 'tly', 'tpi', 
                'tsn', 'tuk', 'tvl', 'twi', 'tyv', 'udm', 'uig', 'umb', 
                'unk', 'uzb', 'wbp', 'wol', 'wuu', 'xal', 'xho', 'xmf', 
                'yap', 'yij', 'yor', 'yua', 'zha', 'zul', 'zza']
                
DK_LANGUAGES = ['aar', 'abk', 'abq', 'ace', 'ach', 'ady', 'afr', 'agr', 
                'aka', 'akl', 'akz', 'ale', 'alt', 'ami', 'aqc', 'ara', 
                'arg', 'arw', 'arz', 'asm', 'ava', 'aym', 'aze', 'bak', 
                'bal', 'bam', 'bcl', 'bel', 'ben', 'bis', 'bod', 'bos', 
                'bre', 'bua', 'bug', 'bul', 'cat', 'ceb', 'ces', 'cha', 
                'che', 'chk', 'chm', 'cho', 'chv', 'cic', 'cjs', 'cor', 
                'crh', 'cym', 'dan', 'dar', 'deu', 'dsb', 'eng', 'est', 
                'eus', 'ewe', 'fao', 'fas', 'fij', 'fil', 'fin', 'fra', 
                'frr', 'fry', 'fur', 'gaa', 'gag', 'gla', 'gle', 'glg', 
                'grc', 'grn', 'gsw', 'guj', 'hak', 'hat', 'hau', 'haw', 
                'hbs', 'heb', 'hil', 'hin', 'hit', 'hrv', 'hun', 'iba', 
                'ilo', 'ind', 'inh', 'isl', 'ita', 'jam', 'jav', 'kaa', 
                'kab', 'kal', 'kan', 'kaz', 'kbd', 'kea', 'ket', 'khb', 
                'kin', 'kir', 'kjh', 'kom', 'kum', 'kur', 'lat', 'lav', 
                'lin', 'lit', 'lld', 'lug', 'luo', 'lus', 'lzz', 'mah', 
                'mal', 'mar', 'mkd', 'mlg', 'mlt', 'mnk', 'mns', 'moh', 
                'mon', 'mri', 'msa', 'mus', 'mww', 'mya', 'myv', 'mzn', 
                'nah', 'nap', 'nau', 'nci', 'nds', 'nep', 'new', 'nia', 
                'niu', 'nld', 'nob', 'non', 'nor', 'nso', 'oci', 'oss', 
                'osx', 'pag', 'pam', 'pan', 'pau', 'pol', 'pon', 'por', 
                'ppl', 'prs', 'pus', 'que', 'roh', 'rom', 'ron', 'rtm', 
                'rus', 'ryu', 'sac', 'sah', 'san', 'sat', 'scn', 'sei', 
                'slv', 'sme', 'sna', 'snd', 'som', 'sot', 'spa', 'sqi', 
                'srd', 'srp', 'sun', 'swa', 'swe', 'tam', 'tat', 'tay', 
                'tel', 'tgk', 'tgl', 'tir', 'tkl', 'tly', 'tpi', 'tsn', 
                'tuk', 'tur', 'tvl', 'twi', 'tyv', 'udm', 'uig', 'ukr', 
                'umb', 'unk', 'urd', 'uzb', 'vie', 'wbp', 'wol', 'wuu', 
                'xal', 'xho', 'xmf', 'yap', 'yid', 'yij', 'yor', 'yua', 
                'yue', 'zha', 'zho', 'zul', 'zza']

@np.vectorize
def levenshtein(a, b):
    """
    computes the levenshtein distance between sequences a and b.
    New: it's broadcastable!
    """
    d = [[0 for i in range(len(b) + 1)] for j in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        d[i][0] = i
    for j in range(1, len(b) + 1):
        d[0][j] = j
    for j in range(1, len(b) + 1):
        for i in range(1, len(a) + 1):
            # future: abstraction. cost depends on phoneme similarity
            cost = int(a[i - 1] != b[j - 1])
            d[i][j] = min(d[i][j - 1] + 1, d[i - 1][j] + 1, d[i - 1][j - 1] + cost)
    return d[len(a)][len(b)]

def per(results):
    """
    results: DataFrame containing at minimum columns for predicted and
            gold standard phoneme sequences
    returns: phoneme error rate of the predictions
    """
    # this is one of two possible ways to compute PER
    return levenshtein(results['predicted'], results['gold']).sum() / results['gold'].apply(len).sum()

def wer(results):
    """
    results: DataFrame containing at minimum columns for predicted and
            gold standard phoneme sequences
    returns: word error rate of the predictions
    """
    return (results['predicted'] != results['gold']).sum() / results['predicted'].size
        
def language_labels(source_file):
    with open(source_file) as f:
        return pd.Series([line.split(None, 1)[0] for line in f])
        
def read_words(corpus_file):
    with open(corpus_file) as f:
        return pd.Series([line.strip().split() for line in f])
    
def output_table(model_path):
    """
    model_path: model directory, containing the corpus subdirectory and the
                results on src.test
    returns: DataFrame whose rows are (language, gold phonemes, predicted phonemes)
    """
    source_test = join(model_path, 'corpus', 'src.test')
    target_test = join(model_path, 'corpus', 'tgt.test')
    predicted_test = join(model_path, 'predicted.txt')
    
    lang_id = language_labels(source_test)
    gold_words = read_words(target_test)
    predicted_words = read_words(predicted_test)

    return pd.DataFrame.from_items([('lang', lang_id), ('gold', gold_words), ('predicted', predicted_words)])
    
def corpus_size(data, index_to_use=None):
    """
    data: src.train or src.test file
    returns quantity of training data per language
    """
    training_size = language_labels(data).value_counts()
    if index_to_use is not None:
        training_size = training_size[index_to_use].fillna(0)
    return training_size.astype('int64')
    
def raw_output(model_path):
    """
    returns a table containing columns for the language, predicted phonemes,
    and gold phonemes for the given model
    """
    source_test = join(model_path, 'corpus', 'src.test')
    target_test = join(model_path, 'corpus', 'tgt.test')
    predicted_test = join(model_path, 'predicted.txt')
    
    lang_id = language_labels(source_test)
    gold_words = read_words(target_test)
    predicted_words = read_words(predicted_test)
    
    return pd.DataFrame.from_items([('lang', lang_id), ('gold', gold_words), ('predicted', predicted_words)])
    
def evaluate(model_path):
    """
    model_path: model directory, containing the corpus subdirectory and the
                results on src.test
    returns: DataFrame containing error rates and the quantity of training data per language
    """
    source_train = join(model_path, 'corpus', 'src.train')
    source_test = join(model_path, 'corpus', 'src.test')
    results = raw_output(model_path)
    training_counts = corpus_size(source_train, results['lang'].unique())
    test_counts = corpus_size(source_test, results['lang'].unique())
    phones = results.groupby('lang').apply(per)
    words = results.groupby('lang').apply(wer)
    return pd.DataFrame.from_items([('wer', words), ('per', phones), ('training_size', training_counts), ('test_size', test_counts)])
    
if __name__ == '__main__':
    import sys
    model_path = sys.argv[1]
    #languages = HIGH_RESOURCE + LOW_RESOURCE
    #exclude = {'umb', 'iba', 'pam', 'bam', 'tay', 'cho'}
    languages = ['<{}>'.format(lang) for lang in DK_LANGUAGES]
    
    model_stats = evaluate(model_path)
    model_stats = model_stats.loc[languages,:]
    print(model_stats.mean())
    model_stats.sort_values(by='per').to_csv(join(model_path, 'results.csv'), sep='\t')
