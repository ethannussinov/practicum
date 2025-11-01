# Author Attribution via Stylometric and Embedding-Based Fingerprints

## Project Overview
The aim of this project is to develop a data science pipeline that can attribute anonymized texts to their most likely author using various stylometric features – such as word choice, punctuation habits, sentence length, and syntactic patterns. The bulk of the project lies at the intersection of natural language processing, literary analysis, and authorship forensics. Possible real world applications include identification of ghostwriters, plagiarism detection, and verification of AI-generated content. This project will compare traditional stylometric methods with modern embedding based techniques (Doc2Vec, BERT) to assess their effectiveness in authorship attribution.

## Current Research Questions
1. Which linguistic features are most indicative of an author's writing style?
2. Can a model reliably distinguish between authors within similar genres or contexts?
3. What are the limitations of stylometric models in generalization and interpretability?

## Features of Interest
1. Lexical Features:
    - `avg_wrd_lngth`, average word length
    - `typ_tkn_rt`, type-token ratio
    - `hpx_lgmn`, hapax legomena
    - `vcb_rch`, vocabulary richness
    - `vcb_cmplx`, vocabulary complexity
2. Syntactic Features:
    - `avg_snt_lngth`, average sentence length
    - `pnct_freq`, punctuation frequency
    - `pos_tag`, part of speech tag patterns
3. Character Level Features:
    - `


## Modeling Approaches
1. Classical Models: Logistic Regression, Random Forest, SVM
2. Neural Models: LSTM, CNN 
3. Similarity Based Models: Doc2Vec, BERT CLS Vectors