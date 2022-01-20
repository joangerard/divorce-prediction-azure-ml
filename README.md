
# Divorce Prediction

Are we going to divorce or not? That's the question we want to answer with this project. 

This project will use both HyperDrive and AutoML which are tools provided by Azure ML. We import the [divorce-prediction dataset](https://www.kaggle.com/andrewmvd/divorce-prediction) into our workspace, we train a model using AutoML, we compare which of them is performing better (higher accuracy), we deploy such model using AzureSDK, and finally, we test the model end point sending fake data and getting a divorce prediction in exchange.

A diagram of the project overview is found below. 

![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/2.png)

## Project Set Up and Installation
1. [Download the Dataset](https://www.kaggle.com/andrewmvd/divorce-prediction) and upload it into the Datasets section in your Machine Learning Studio. 
2. Create a compute instance and open jupyter.
3. Open a new terminal and clone the project into your compute instance.
4. Download the config.json file from your workspace and replace it.
5. Execute the hyper-drive and the auto-ml jupyter notebooks.

## Dataset

### Overview
We use the [divorce prediction data set](https://www.kaggle.com/andrewmvd/divorce-prediction) from Kaggle to train the models that consists in 54 questions, everyone should be answered in a scale from 0 to 4 and the outcome indicates if the couple will or not divorce. 

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
![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/6.png)

![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/2.png)

Once the pipeline finishes to run we can see what models were used by AutoML: 

![models](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/5.png)

Also we can retrieve the best model together with its parameters via AzureSDK:

![parameters](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/4.png)

The model is also available on the Machine Learning Studio:

![model](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/3.png)

We can also use the `get_output()` function to obtain information about the best model run id:

![model](https://github.com/joangerard/project-azure-piepline/blob/master/images/automl/7.png)

## Hyperparameter Tuning
Random Forest was chosen to predict the outcome because it's an ensemble model that uses many decision trees and then averages the result of their individual predictions. 

The parameters to be tuned were: 
- The number of estimators: from a random choice among 500,1000,1500,2000,and 3000
- Max Depth: from a random choice among 10,50,100,and 150
- Min Samples Split: from a random choice among 2, 5, and 7

A Bandit Policy was also used to enable early stop.

12 runs were used executed using 4 concurrent runs.

### Results
The best model gave an accuracy of 0.99 with:
- 3000 estimators
- A max depth of 100
- 2 min samples split

Here we can see the RunDetails widget display showing that 12/12 hypothesis (runs) were already tested. The run 23 gave the best accuracy with 0.99. 

![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/hyperdrive/1.png)

Here we can see more graphical information about the parameters and their accuracy when running the model with different parameters:

![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/hyperdrive/2.png)

![RunDetails](https://github.com/joangerard/project-azure-piepline/blob/master/images/hyperdrive/3.png)

We can also see the best parameters configuration and its accuracy:
![best parameters configuration](https://github.com/joangerard/project-azure-piepline/blob/master/images/hyperdrive/4.png)

We are obtaining high accuracy because the higher the number that answers the question, more are the chances to get divorced then it's easy for the random forest model to learn such a thing. We could improve the model incrementing the number of runs.

## Model Deployment
Both models (automl-hyperdrive) were registered.

![best parameters configuration](https://github.com/joangerard/project-azure-piepline/blob/master/images/1.png)

### Deployment
Since the hyperdrive model gave a better accuracy, that's the one which is deployed. 
In order to deploy it we need to:
- Create an environment with the needed packages dependencies.
- Create a deployment configuration file (LocalWebservice or AciWebservice): it's a good practice to deploy the model in a local webservice first, verify that it is working and then deploy it into an Azure Computer Instance (for development) or Azure Kubernates Instance (for production). If AciWebservice is being used we can here enable authentication and also app insights.
- Create an inference config file that receives an entry script and the environment previosly created. The entry script is the script that will be executed when the API receives a request. It has two methods: init and run. The run method should receive the data body, process it and return the prediction made by the model previously loaded in the init method. 
- Deploy the model providing the workspace, a name for the service, the registered model, the inference configuration, and the deployment configuration.


We can see here the deployed model showing an status of healthy indicating that it is active and ready to be consumed using its provided REST endpoint.
![model](https://github.com/joangerard/project-azure-piepline/blob/master/images/hyperdrive/5.png)

### Consume API
In order to consume the deployed web service, we need to:
- We can access the swagger uri that will provide information about how to use the API.
- Create a json data with the answers to the 54 questions into an array.
- Send a request to the API url using the configured headers, authorization bearer api key and the body encoding the json data. 
- Once the API returns a response parse it and display it. If an error occures print information about it.

A sample input of three quiz answers will be send in the body such as:
```
{
  "data": [
    [1,4,3,2,4,2,1,4,...,4,3],
    [3,2,3,1,3,4,3,2,...,3,4],
    [1,4,1,1,1,0,0,1,...,0,1]
  ]
}
```
Every array corresponds to 54 elements containing the answer, each element from 0 to 4 corresponding to the answer to an individual question.

A sample response will consist of a number for every quiz sent, corresponding to the prediction that the couple will or not divorce. Numbers closer to 1 means the couple will divorce whereas numbers closer to 0 means the couple will not divorce.

```
[0.99, 0.65, 0.05]
```

The model predicst that the first couple will divorce, the second has many chances to get divorced, and the last one might not divorce at all. 

## Future Improvement Suggestions
The project can be improved in many ways. 
- The train.py script uses all 54 features to train a random forest model. We could do feature engineering here to work with only those features that are relevant for the prediction. 
- The REST endpoint that uses the score.py file to make a prediction could have validated the data before feeding it into the model. Each value should be between 0 and 4. 
- The process of selecting which model is more acurate, HyperDrive or AutoML, can be automatized using a pipeline for automatically check on the best accuracy and select that model to be deployed. 

## Screen Recording
You can see a brief explanation about the project [here](https://www.youtube.com/watch?v=4ojXFhMVkq4).

