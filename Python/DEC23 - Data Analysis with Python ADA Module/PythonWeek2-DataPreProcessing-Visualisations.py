import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop') #Here I am creating a file path to the users desktop and im making sure not to hard code this so it works for the assessor.

# I am loading the datasets below using variables assigned to reading the corrsponding csv files.
train_data = pd.read_csv(os.path.join(desktop_path, 'train.csv'))
test_data = pd.read_csv(os.path.join(desktop_path, 'test.csv'))
gender_submission = pd.read_csv(os.path.join(desktop_path, 'gender_submission.csv'))

print("Train Data:") # Display basic information about the datasets
print(train_data.info())
print("\nTest Data:")
print(test_data.info())
print("\nGender Submission Data:")
print(gender_submission.info())

print("\nFirst few rows of Train Data:")# Display the first few rows of the datasets
print(train_data.head())
print("\nFirst few rows of Test Data:")
print(test_data.head())
print("\nFirst few rows of Gender Submission Data:")
print(gender_submission.head())

# I am checking for any missing values with the small block of code below
print("\nMissing values in Train Data:")
print(train_data.isnull().sum())
print("\nMissing values in Test Data:")
print(test_data.isnull().sum())

plt.figure(figsize=(12, 8))  # Visualising the distribution of age using a histogram
sns.histplot(train_data['Age'].dropna(), kde=True)
plt.title('Distribution of Age')
plt.show()

plt.figure(figsize=(12, 8)) # Here I am visualising the number of peoplw who survived and died.
sns.countplot(x='Survived', data=train_data)
plt.title('Survival Count')
plt.show()

plt.figure(figsize=(12, 8)) # This code is visualising the distibution of passengers amongst the different classes (Pclass)
sns.countplot(x='Pclass', data=train_data)
plt.title('Passenger Class Distribution')
plt.show()

plt.figure(figsize=(12, 8)) # Count of male and female passengers
sns.countplot(x='Sex', data=train_data)
plt.title('Count of Male and Female Passengers')
plt.show()

plt.figure(figsize=(12, 8))#Distribution of fare prices
sns.histplot(train_data['Fare'], kde=True)
plt.title('Distribution of Fares')
plt.show()

# Exclude non-numeric columns before calculating correlation
numeric_columns = train_data.select_dtypes(include=['float64', 'int64']).columns
correlation_matrix = train_data[numeric_columns].corr()

# Here i am exploring the relationships between the features in the dataset.
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Correlation Matrix')
plt.show()
