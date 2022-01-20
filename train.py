#!/usr/bin/env python
# coding: utf-8
# %%
# azureml-core of version 1.0.72 or higher is required
# azureml-dataprep[pandas] of version 1.1.34 or higher is required
from azureml.core import Workspace, Dataset
# Import the model we are using
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import argparse
import numpy as np
import joblib
from azureml.data.dataset_factory import TabularDatasetFactory
from azureml.core.run import Run

# azureml-core of version 1.0.72 or higher is required
# azureml-dataprep[pandas] of version 1.1.34 or higher is required
from azureml.core import Workspace, Dataset

dataset = TabularDatasetFactory.from_delimited_files(path='https://raw.githubusercontent.com/joangerard/project-azure-piepline/master/divorce_data.csv', separator=';')
df = dataset.to_pandas_dataframe()
df = df.sample(frac=1)


# %%


run = Run.get_context()


# %%


x = df.iloc[:,:-1]
y = df.iloc[:,-1]


# %%


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# %%
parser = argparse.ArgumentParser()
parser.add_argument('--e', type=int, default=1000, help="Number of estimators")
parser.add_argument('--md', type=int, default=100, help="Max Depth")
parser.add_argument('--msp', type=int, default=5, help="Min Samples Split")
args = parser.parse_args()

run.log('Number of estimators', np.int(args.e))
run.log('Max Depth', np.int(args.md))
run.log('Min Samples Split', np.int(args.msp))

# Instantiate model with 1000 decision trees
rf = RandomForestRegressor(n_estimators = args.e, max_depth=args.md, min_samples_split=args.msp, random_state = 42)
# Train the model on training data
rf.fit(X_train, y_train);


# %%
joblib.dump(value=rf, filename="./outputs/model.joblib")

accuracy = rf.score(X_test, y_test)
run.log("Accuracy", accuracy)




