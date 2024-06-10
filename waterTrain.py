import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import pickle
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("datasets/water_potability.csv")

df["ph"] = df['ph'].fillna(df['ph'].mean())
df["Sulfate"] = df["Sulfate"].fillna(df["Sulfate"].mean())
df["Trihalomethanes"] = df["Trihalomethanes"].fillna(df["Trihalomethanes"].mean())
print(df.head())

print("wtr1")
selected_columns = ['ph', 'Solids', 'Conductivity', 'Potability']
df_use = df[selected_columns]
x = df_use.drop("Potability", axis=1)
y = df_use["Potability"]
print(x.head())
print(y.head())

print("wtr2")
scaler = StandardScaler()
x = scaler.fit_transform(x)
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2)

print("wtr3")
waterSVM = SVC(kernel="rbf")
waterSVM.fit(x_train, y_train)

print("wtr4")
y_pred = waterSVM.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Accuracy:", accuracy * 100)
print("Precision:", precision * 100)
print("Recall:", recall * 100)
print("F1_Score:", f1 * 100)

with open('svm_model.pkl', 'wb') as f:
    pickle.dump(plt.clf, f)