import numpy as np
import random
# MUT_RATE = 0.8

def mutation(dna):
  new_dna = [1]
  # l = len(dna)
  for gene in dna[1:]:
    # if random.random() < MUT_RATE:
    new_gene = np.random.normal(gene, abs(gene/4))
    # else:
      # new_gene = gene
    new_dna.append(new_gene)
  
  return new_dna


# print(mutation([1, -25.325022444744448, -18.910244652970754, 7.445442416402557, -4.333884632099817, -38.34886938819313, 44.68325977924911, -18.85197492477182, -19.217581927107208, -5.99130591515388, -42.75038542477261, 39.21641724976254, 25.991296901008553, -1.7570549368093324, 2.417098781266901, 12.377498130863984, -27.293029039722448]))
