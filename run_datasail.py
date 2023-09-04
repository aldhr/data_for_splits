import joblib
import os
import pandas as pd
from datasail.sail import datasail

# Load your data
df = pd.read_csv('splits_db.tsv', sep='\t')

# List of techniques to iterate through
techniques = ["ICD"]# "ICD", "CCSf", "CCD"]

# Iterate through each technique
for technique in techniques:
    e_splits, f_splits, inter_splits = datasail(
        techniques=[str(technique)],
        splits=[7, 2, 1],
        names=["train", "val", "test"],
        runs=1,
        solver="SCIP",
        inter=[(x[0], x[0]) for x in df[["ids"]].values.tolist()],
        e_type="M",
        e_data=dict(df[["ids", "Ligand"]].values.tolist()),
        f_type="P",
        f_data="pdbs",
    )

    # Create a new folder if it doesn't exist
    new_folder = 'split_by_' + technique
    os.makedirs(new_folder, exist_ok=True)

    # Save the dictionaries to files using joblib in the new folder
    joblib.dump(e_splits, os.path.join(new_folder, 'e_splits.joblib'))
    joblib.dump(f_splits, os.path.join(new_folder, 'f_splits.joblib'))
    joblib.dump(inter_splits, os.path.join(new_folder, 'inter_splits.joblib'))

