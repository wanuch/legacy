import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
import matplotlib.pyplot as plt # this is used for the plot the graph 
import seaborn as sns # used for plot interactive graph. I like it most for plot
get_ipython().magic('matplotlib inline')
from sklearn.linear_model import LogisticRegression # to apply the Logistic regression
from sklearn.model_selection import train_test_split # to split the data into two parts
#from sklearn.cross_validation import KFold # use for cross validation
from sklearn import metrics # for the check the error and accuracy of the model
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# read data from a csv file
data = pd.read_csv('../desktop/breast-cancer-wisconsin.csv', header=0)

# Do not need to analyst id_number
data.drop("Id",axis=1,inplace=True)

# Show 5 upper data 
data.head(5)

print(data.shape)

# Show data describtion
data.describe()

# Show data information
data.info()

data.columns

# Define Malignant(M) = 4, benign(B) = 2
data['Class'] = data['Class'].map({4:4,2:2})

# Show graph between Malignant(M) = 4 and benign(B) = 2
sns.countplot(data['Class'], label="Count")

# Show the general gaussian distribution
data.plot(kind='density', subplots=True, layout=(5,7), sharex=False, legend=False, fontsize=1)
plt.show()

Y = data['Class'].values
X = data.drop('Class', axis=1).values

# Randomly 80% sample of the training and testing it on the remaining 20%.
X_train, X_test, Y_train, Y_test = train_test_split (X, Y, test_size = 0.2, random_state=21)

# Check the number of the training and testing sample
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

plt.scatter(X_test[:,0], X_test[:,1], s=40, c=Y_test, cmap=plt.cm.plasma)

# Set iteration = 10 and train it
LogReg = LogisticRegression(max_iter=10)
LogReg.fit(X_train, Y_train)

Y_prediction = LogReg.predict(X_test)

confusion_matrix = confusion_matrix(Y_test, Y_prediction)
confusion_matrix

# Summary of the precision, recall, F1 score for each disngosis
print(classification_report(Y_test, Y_prediction))

