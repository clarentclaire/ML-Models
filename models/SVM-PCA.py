# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:00:20 2020

@author: user
"""

# SVM - PCA
  # PCA : Dimensionality reduction
  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import datasets 
from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from matplotlib.colors import ListedColormap
from sklearn.decomposition import PCA

filename = 'D:\\ClarentiCelsia\\Personal\\SKRIPSI\\Image Classification\\dataset\\diabetes.csv'

def pca():
  
    # READ CSV 
    diabetes = pd.read_csv(filename)
       #print(diabetes) : to see the table
       
    # DEPENDENT VARs
    X = diabetes.iloc[:, :8]
    # INDEPENDENT VAR : Outcome
    y = diabetes['Outcome']
 
    # Splitting the data into training, and testing set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    print("training set: ", X_train.shape)
    print("testing set: ", X_test.shape)
    
    # Feature scalling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
   
    # Reduce dimension into 2D
    pca = PCA(n_components = 2)
    pca.fit(X_train)

    # Standardizing
    X_train = pca.fit_transform(X_train)
    X_test = pca.fit_transform(X_test)
    
    # PCA Results
    print("Features after reducing by PCA 2D: ", X_train, "\n")
    
    # Dataframe
      # data = dataname
      # columns = column name
      # axis = 1 (insert right/left) : cols
    #X_train_table = pd.DataFrame(data = pca_train, columns=[x1, x2])
    #concatenate_label_to_x_train = pd.concat([X_train_table, y_train.iloc[:,0]], axis = 1) 
    
    #sns.lmplot('pca1', 'pca2', data=pca_train, hue='label', palette='Set1', fit_reg=False, scatter_kws={'s': 2})
    
    # VIsualize the dataset after reduction
    plt.figure(figsize=(20,15))
    X_set, y_set = X_train, y_train
    
    for i, j in enumerate(np.unique(y_set)):
       plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], c = ListedColormap(('red', 'green'))(i), label = j)
    
    plt.xlabel('1st principal component')
    plt.ylabel('2nd principal component')
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()
    
    model(X_train, X_test, y_train, y_test)


def model(X_train, X_test, y_train, y_test):
    # Build model
    svm = SVC(kernel='linear', probability=True)
    svm.fit(X_train, y_train)
    
    # Visualize support vectors of training set
    support_vectors = svm.support_vectors_

    plt.scatter(X_train[:,0], X_train[:,1])
    plt.scatter(support_vectors[:,0], support_vectors[:,1], color='blue')
    plt.title('Support Vectors')
    plt.xlabel('X')
    plt.ylabel('y')
    plt.show()
    
    # Visualize training & Testing set
      # Replace X_set, y_set according to the visualization 
    X_set, y_set = X_train, y_train
    X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),\
                         np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
    plt.contourf(X1, X2, svm.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape), alpha = 0.75, cmap = ListedColormap(('red', 'green')))
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    
    for i, j in enumerate(np.unique(y_set)):
       plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], c = ListedColormap(('red', 'green'))(i), label = j)
           
    plt.title('SVM (training)')
    plt.xlabel('1st pca')
    plt.ylabel('2nd pca')
    plt.legend()
    plt.show()
    
    print("\n")

    # Predict
    y_pred = svm.predict(X_test)
    # Accuracy
    test_accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy of prediction: ", test_accuracy)
    
  
    # Figure out the confusion matrix suchas recall, precision,..
    confusionmatrix = confusion_matrix(y_test, y_pred)
    print("The confusion matrix: ", confusionmatrix)
    
    print("\n")
    # Evaluating by using Cross val on Training Set & Testing set
    test_scores = cross_val_score(svm, X_test, y_test, scoring='accuracy', cv=5)
    print("Accuracy of testing set by using cross val : ",test_scores)
    print("Mean of test scores: ", test_scores.mean())
    
    print("\n")
    
    # Cross checking back
    # Check the probability of prediction value
    predict_proba_value = svm.predict_proba(X_test) 
    y_pred_valid = svm.predict(X_test)  
    
    print("what value of prediction probability so system can determine which class of them: ", predict_proba_value)
    print("what system predicts toward the validating set of svm: ", y_pred_valid)
  
    

if __name__ == "__main__":   
    pca()
    print("\n")

    
    
"""
Axis 0 : cols
Axis 1 : rows
"""

    
    
