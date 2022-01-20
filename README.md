
# Divorce Prediction

Are we going to divorce or not? That's the question we want to answer with this project. 

## Project Set Up and Installation
1. Download the Dataset and upload it into the Datasets section in your Machine Learning Studio. 
2. Create a compute instance and open jupyter.
3. Open a new terminal and clone the project into your compute instance.
4. Download the config.json file from your workspace and replace it.
5. Execute the hyper-drive and the auto-ml jupyter notebooks.

## Dataset

### Overview
We use the [divorce prediction data set ](hhttps://www.kaggle.com/andrewmvd/divorce-prediction) from Kaggle to train the models that consists in 54 questions, everyone should be answered in a scale from 0 to 4 and the outcome indicates if the couple will or not divorce. 

### Task
All the features are used from the dataset to predict the output(0/1) that indicates if the couple will or not divorce baset on the answers provided to the questions.

### Access
The data is uploaded into the Dataset section in the Machine Learning Studio. This is consumed by the auto-ml script. In case it does not find it, it will use [this public url](https://raw.githubusercontent.com/joangerard/project-azure-piepline/master/divorce_data.csv) that points to the dataset uploaded to this github repository. That's not the case for the hyper-drive script that executes an external Python script (train.py). This script uses directly the public url aforementioned.

## Automated ML
The experiment time out was configured to be 20 minutes and the metric to be used is the accuracy. The label column is the 'Divorce' one. Early stopping is enabled to avoid a bad model to continue training.

A pipeline was created to obtain metrics information and the best model output. These are the output of the AutoMLStep. The model was then saved and registered.

### Results
The best model that AutoML found was after performing Max Absolute Scaler and the passing the data through a Random Forest Classifier with 200 estimators using bootstrap. The accuracy of such model was 0.988. We could have obtained a better performance by increasing the timeout to let AutoML experiment with more models/parameters. 

Here we can see the RunDetails widget display that shows how the AutoML pipeline is still running. Below there we can see a graph that shows the steps followed by the pipeline which is reading the divorce dataset and pass it to the AutoML step.
![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/1.png)

![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/2.png)

Once the pipeline finishes to run we can see what models were used by AutoML: 

![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/5.png)

Also we can retried the best model together with the parameters used via AzureSDK:

![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/4.png)

The model is also available on the Machine Learning Studio:

![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/3.png)
*TODO* Remeber to provide screenshots of the `RunDetails` widget as well as a screenshot of the best model trained with it's parameters.

## Hyperparameter Tuning
*TODO*: What kind of model did you choose for this experiment and why? Give an overview of the types of parameters and their ranges used for the hyperparameter search


### Results
*TODO*: What are the results you got with your model? What were the parameters of the model? How could you have improved it?

*TODO* Remeber to provide screenshots of the `RunDetails` widget as well as a screenshot of the best model trained with it's parameters.

## Model Deployment
*TODO*: Give an overview of the deployed model and instructions on how to query the endpoint with a sample input.

## Screen Recording
*TODO* Provide a link to a screen recording of the project in action. Remember that the screencast should demonstrate:
- A working model
- Demo of the deployed  model
- Demo of a sample request sent to the endpoint and its response

## Standout Suggestions
*TODO (Optional):* This is where you can provide information about any standout suggestions that you have attempted.
