import sys
import pandas as pd
import numpy as np
import os

def topsis(input_file, weights, impacts, output_file):

   
    if not os.path.exists(input_file):
        print("Error: Input file not found")
        sys.exit(1)

    data = pd.read_csv(input_file)

   
    if data.shape[1] < 3:
        print("Error: Input file must contain at least 3 columns")
        sys.exit(1)

    
    try:
        matrix = data.iloc[:, 1:].astype(float).values
    except:
        print("Error: Non-numeric values in criteria columns")
        sys.exit(1)

    weights = weights.split(",")
    impacts = impacts.split(",")

 
    if len(weights) != matrix.shape[1] or len(impacts) != matrix.shape[1]:
        print("Error: Weights, impacts and criteria count must match")
        sys.exit(1)

   
    for i in impacts:
        if i not in ['+', '-']:
            print("Error: Impacts must be + or -")
            sys.exit(1)

    weights = np.array(weights, dtype=float)


    norm = matrix / np.sqrt((matrix ** 2).sum(axis=0))


    weighted = norm * weights


    ideal_best = []
    ideal_worst = []

    for j in range(weighted.shape[1]):
        if impacts[j] == '+':
            ideal_best.append(weighted[:, j].max())
            ideal_worst.append(weighted[:, j].min())
        else:
            ideal_best.append(weighted[:, j].min())
            ideal_worst.append(weighted[:, j].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)


    d_pos = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = d_neg / (d_pos + d_neg)

    data["Topsis Score"] = score
    data["Rank"] = data["Topsis Score"].rank(ascending=False).astype(int)

    data.to_csv(output_file, index=False)
    print("Result saved in", output_file)

if len(sys.argv) != 5:
    print("Usage: python topsis.py <InputFile> <Weights> <Impacts> <OutputFile>")
    sys.exit(1)

topsis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

