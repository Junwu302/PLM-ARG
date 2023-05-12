
# PLM-ARG: Antibiotic Resistance Gene Identification using a pretrained protein language model

![Fig 1.png](https://img1.imgtp.com/2023/05/12/jppD7XGg.png)

## 1. Training data collection
We incorporated and standardized the collected AGRs from five databases including CARD (Release Date: 05/27/2022) <sup>[1]</sup>, ResFinder (Release Date: 24/05/2021)<sup>[2]</sup>, MEGARes (Release Date: 14/10/2019)<sup>[3,4]</sup>, ARGMiner (Release Version: v1.1.1.A)<sup>[5]</sup>, AMRFinderPlus (Release Date: 11/08/2021)<sup>[6]</sup> and HMD-ARG-DB<sup>[7]</sup>(Fig. 2A). First, considering that various genomic technologies detected the ARGs in these databases, we converted all ARGs with DNA sequence format into UniPort FASTA protein sequence format using EMBOSS tool Transeq. Then, we removed the duplicated ARGs by clustering all their sequences with CD-HIT and discarding duplicates with 100% identity and the same length. Finally, resistance categories of ARGs were assigned based on their conferred antibiotic drug classes with manual correction based on the WHO access, watch, reserve, classification of antibiotics for evaluation and monitoring of use (AWaRe) classification system (https://apps.who.int/iris/rest/bitstreams/1374989/retrieve). 
## 2. Model architecture
For each protein sequence, we represented it as a embedding vector using a transformer protein language model [ESM-1b](https://github.com/facebookresearch/esm), which is built based on the RoBERTa architecture and training procedure using the Uniref50 protein sequences without label supervision. To reduce the computational complexity, the proteins longer than 200 amino acids were trimmed into a fix length 200 amino acids before fed into the ESM-1b model. We generated per-sequence representations via averaging the output of the 32nd layer of ESM-1b model over the full sequence and yielding a 1280-length numeric vector for each protein. After that, we trained XGboost model for ARG identification and resistance category classification respectively using the whole PLM-ARGDB as well as the Non-ARGs mentioned above.
## 3. Code usage
To use the PLM-ARG codes, you first need to download the 'esm1b_t33_650M_UR50S.pt' and put it under the fold of 'models/'.
### 1) Predicting ARG using the pre-trained models. 
Just run the following command:
```bash
python plm_arg.py predict -i proteins.faa --arg-model models/arg_model.pkl --cat-model models/cat_model.pkl --cat-index models/Category_Index.csv -o plm_arg_res.tsv --min-prob 0.5 -b 10
```
or run the following command with default parameters:
```bash
python plm_arg.py predict -i proteins.faa -o plm_arg_res.tsv
```
### 2) Retraining the PLM-ARG models with your own data
You first need to make sure that your fasta file header follows this schema:\
`>gene_id|source|arg_category|arg_name|arg_group`
Putting your training sequences (e.g. arg_db.faa) in the 'db/' fold and run the following command.
```bash
python plm_arg.py train -i proteins.faa --arg-model models/arg_model.pkl --cat-model models/cat_model.pkl --cat-index models/Category_Index.csv --min-seq 50 -b 10
```
or run the following command with default parameters:
```bash
python plm_arg.py train -i arg_db.faa
```
## 4. Web server
We have released a web service to process gene sequence or predicted ORF using PLM-ARG. You can find the website at http://www.unimd.org/PLA_ARG PLM-ARG takes the gene sequence or predicted ORF as the input and output including both the resistance categories (if the query was classified as ARG) and the corresponding probability.
## 5. PLM-ARG output
The ouput of PLM-ARG contains the the probability of the query proteins predicted as ARG, and the probability respect to different resistance category if the ARG probability >= 0.5 (default).   

## 6. Dependencies
- python                    3.7.13
- pytorch                   1.11.0
- fair-esm                  0.4.2
- joblib                    1.1.0
- numpy                     1.21.5
- pandas                    1.3.5
- xgboost                   1.6.1
- scikit-learn              1.0.2

#### Reference 
[1] Alcock, B.P., Raphenya, A.R., Lau, T.T.Y., Tsang, K.K., Bouchard, M., Edalatmand, A., Huynh, W., Nguyen, A.V., Cheng, A.A., Liu, S. et al. (2020) CARD 2020: antibiotic resistome surveillance with the comprehensive antibiotic resistance database. Nucleic Acids Res, 48, D517-D525.\
[2]	Kleinheinz, K.A., Joensen, K.G. and Larsen, M.V. (2014) Applying the ResFinder and VirulenceFinder web-services for easy identification of acquired antibiotic resistance and E. coli virulence genes in bacteriophage and prophage nucleotide sequences. Bacteriophage, 4, e27943.\
[3]	Doster, E., Lakin, S.M., Dean, C.J., Wolfe, C., Young, J.G., Boucher, C., Belk, K.E., Noyes, N.R. and Morley, P.S. (2020) MEGARes 2.0: a database for classification of antimicrobial drug, biocide and metal resistance determinants in metagenomic sequence data. Nucleic Acids Res, 48, D561-D569\
[4] Lakin, S.M., Dean, C., Noyes, N.R., Dettenwanger, A., Ross, A.S., Doster, E., Rovira, P., Abdo, Z., Jones, K.L., Ruiz, J. et al. (2017) MEGARes: an antimicrobial resistance database for high throughput sequencing. Nucleic Acids Research, 45, D574-D580.\
[5] Arango-Argoty, G.A., Guron, G.K.P., Garner, E., Riquelme, M.V., Heath, L.S., Pruden, A., Vikesland, P.J. and Zhang, L. (2020) ARGminer: a web platform for the crowdsourcing-based curation of antibiotic resistance genes. Bioinformatics, 36, 2966-2973.\
[6]	Feldgarden, M., Brover, V., Haft, D.H., Prasad, A.B., Slotta, D.J., Tolstoy, I., Tyson, G.H., Zhao, S., Hsu, C.-H., McDermott, P.F.J.A.a. et al. (2019) Validating the AMRFinder tool and resistance gene database by using antimicrobial resistance genotype-phenotype correlations in a collection of isolates. 63, e00483-00419.\
[7] Li, Y., Xu, Z.L., Han, W.K., Cao, H.L., Umarov, R., Yan, A.X., Fan, M., Chen, H., Duarte, C.M., Li, L.H. et al. (2021) HMD-ARG: hierarchical multi-task deep learning for annotating antibiotic resistance genes. Microbiome, 9.
