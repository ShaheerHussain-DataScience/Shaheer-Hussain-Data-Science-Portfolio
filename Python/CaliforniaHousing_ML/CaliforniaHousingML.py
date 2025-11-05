import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

from sklearn import datasets #Step 1 - import datasets from sklearn
from sklearn.model_selection import train_test_split #Step 5 - import train test split from model selection
from sklearn.linear_model import LinearRegression #Step 9 - import our model of choice, in this case it is linear regression
from sklearn.metrics import r2_score #Step 14 - to evaluate our y_pred against our y_test we need an eval method, for now we will use r2
from sklearn.ensemble import HistGradientBoostingRegressor #Step - 16 Importing GradientBoostingRegressor from ensemble
from sklearn.ensemble import RandomForestRegressor #Step - 17 Importing RandomForestRegressor from ensemble

housing = datasets.fetch_california_housing() #Step 2 - assign our dataset to a  variable

x = housing.data #Step 3 - Assign our features to x
y = housing.target #Step 4 - Assign our target to y


x_train, x_test, y_train, y_test = train_test_split(x , y , test_size=0.2, random_state=500) #Step 6 Making use of our automated train test split function, passing x and y whilst reserving 1/5 or 20% of the dataset for testing
#Step 7 We assign our train test split to the 4 variables x_train, x_test, y_train, y_test to make us eof later
#Step 8 we assign a ransom state parameter so that we shuffle our samples in a specific order to recreate the same workflow over and over (get the same output so its easier to test)

LR = LinearRegression() #Step 10 - initialise our LR model function and assign it to a variable
HGBR = HistGradientBoostingRegressor() #Step 18 - initialise our GBR model function and assign it to a variable
RFR = RandomForestRegressor(n_jobs=-1) #Step 19 - initialise our RFR model function and assign it to a variable / set n_jobs to -1 to use all available cpu cores

for i in [LR, HGBR, RFR]: #Step 20 - use a for loop to fir, predict and evaluate all of our imported models
    i.fit(x_train, y_train) #training our model using x and y train
    y_pred = i.predict(x_test) #Step 12 - we are going to predict (x_test) on data it hasnt seen before / assigning this to y_pred variable
    #Step 13 - its crucial that y_pred knows nothing about y_test as this is what it is trying to predict
    r2 = r2_score(y_test, y_pred) #Step 15 - We will call the r2 function and pass y_test and y_pred for evaluation
    print(i, r2)#Step FINAL - Printing results - initial baseline was an r2 of 0.607 which tell us our model understands 60% of the data / why house prices fluctuate


models = [LR, HGBR, RFR]
model_names = ["Linear Regression", "HistGradientBoosting", "Random Forest"]

for model, name in zip(models, model_names):
    y_pred = model.predict(x_test)
    plt.figure(figsize=(6,5))
    sns.scatterplot(x=y_test, y=y_pred, s=10)
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title(f"Actual vs Predicted - {name}")
    plt.show()


for model, name in zip(models, model_names):
    y_pred = model.predict(x_test)
    residuals = y_test - y_pred

    plt.figure(figsize=(6,5))
    sns.scatterplot(x=y_pred, y=residuals, s=10)
    plt.axhline(0, color="red", linestyle="--")
    plt.xlabel("Predicted Prices")
    plt.ylabel("Residuals")
    plt.title(f"Residual Plot - {name}")
    plt.show()

feature_names = housing.feature_names

# Random Forest Feature Importance
importances = RFR.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(7,5))
sns.barplot(x=importances[indices], y=np.array(feature_names)[indices])
plt.title("Feature Importance (Random Forest)")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.show()


