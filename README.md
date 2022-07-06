# HiARG: Homology Independent Antibiotic Resistance Gene Identification based on a Protein Language Model

[![jUXeg0.png](https://s1.ax1x.com/2022/07/06/jUXeg0.png)](https://imgtu.com/i/jUXeg0)

## 1. Training data collection
We incorporated and standardized the collected AGRs from five databases including CARD (Release Date: 05/27/2022) (34), ResFinder (Release Date: 24/05/2021)<sup>[1]</sup>, MEGARes (Release Date: 14/10/2019) (36,37), ARGMiner (Release Version: v1.1.1.A) (38), AMRFinderPlus (Release Date: 11/08/2021)(39) and HMD-ARG-DB (31) (Fig. 2A). First, considering that various genomic technologies detected the ARGs in these databases, we converted all ARGs with DNA sequence format into UniPort FASTA protein sequence format using EMBOSS tool Transeq (40). Then, we removed the duplicated ARGs by clustering all their sequences with CD-HIT [37] and discarding duplicates with 100% identity and the same length. Finally, resistance categories of ARGs were assigned based on their conferred antibiotic drug classes with manual correction based on the WHO access, watch, reserve, classification of antibiotics for evaluation and monitoring of use (AWaRe) classification system (https://apps.who.int/iris/rest/bitstreams/1374989/retrieve). 
## 2. Model architecture




[1] Alcock, B.P., Raphenya, A.R., Lau, T.T.Y., Tsang, K.K., Bouchard, M., Edalatmand, A., Huynh, W., Nguyen, A.V., Cheng, A.A., Liu, S. et al. (2020) CARD 2020: antibiotic resistome surveillance with the comprehensive antibiotic resistance database. Nucleic Acids Res, 48, D517-D525.
[2]	Kleinheinz, K.A., Joensen, K.G. and Larsen, M.V. (2014) Applying the ResFinder and VirulenceFinder web-services for easy identification of acquired antibiotic resistance and E. coli virulence genes in bacteriophage and prophage nucleotide sequences. Bacteriophage, 4, e27943.
[3]	Doster, E., Lakin, S.M., Dean, C.J., Wolfe, C., Young, J.G., Boucher, C., Belk, K.E., Noyes, N.R. and Morley, P.S. (2020) MEGARes 2.0: a database for classification of antimicrobial drug, biocide and metal resistance determinants in metagenomic sequence data. Nucleic Acids Res, 48, D561-D569
