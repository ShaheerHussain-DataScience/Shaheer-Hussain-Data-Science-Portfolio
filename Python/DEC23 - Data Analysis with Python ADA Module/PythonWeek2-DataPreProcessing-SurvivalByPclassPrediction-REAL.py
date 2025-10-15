import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')#Here I am creating a file path to the users desktop and im making sure not to hard code this so it works for the assessor.

train_data = pd.read_csv(os.path.join(desktop_path, 'train.csv')) # Loading the train csv file which is part of this dataset

# I am just exploring the data to gain a deeper understanding
print("Data Overview:")
print(train_data.head())

# I am selecting my features here
features = ['Pclass']  # Im using 'Pclass' as the feature for predicting survival
target = 'Survived'

train_data = train_data.dropna(subset=[*features, target]) # Dropping rows with missing values for simplicity sake

# Below I am Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    train_data[features], train_data[target], test_size=0.2, random_state=42
)

# Initialize and fit the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Use the model to predict the testing set
y_pred = model.predict(X_test)

#Below I am evaluating the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Display the final results
print(f'Model Accuracy: {accuracy:.2f}')
print('\nConfusion Matrix:')
print(conf_matrix)
print('\nClassification Report:')
print(class_report)
