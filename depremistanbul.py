# -*- coding: utf-8 -*-
"""DepremIstanbul.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Cj9iENDl9xCKZhzG9N6_ZBToLDoIXz4O
"""

import numpy as np                                #Required Libraries Added
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from matplotlib.patches import Patch
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("deprem.csv", encoding="ISO-8859-9", delimiter=";")  #File Included in Page

df.head(3)  #Shows the first 3 rows of the data set

df.tail(3)   #Shows the last 3 rows of the data set

df.info()   #Shows general information of the data set

df.shape  #Returns the dimensions of the data set (number of rows and columns)

df.columns  #Lists the column names in the data set

df.describe().T  #Shows statistical summary of numeric columns by transposing

df.isnull().any()  #Checks which columns have empty values

df["ilce_adi"].value_counts()   #Shows the frequencies of the values in the 'ilce_adi' column

df.groupby("ilce_adi").agg({"can_kaybi_sayisi":"sum"})  #Calculates the total number of casualties for each district

df.groupby(["ilce_adi", "mahalle_adi"]).agg({"can_kaybi_sayisi":"sum"})  #Calculates the total number of casualties for each district and neighborhood

sns.set(style="whitegrid")
palette = sns.color_palette("viridis", len(df['ilce_adi'].unique()))
plt.figure(figsize=(15, 8))
sns.barplot(x="ilce_adi", y="can_kaybi_sayisi", data=df, palette=palette)                         #Creating a bar chart visualizing mortality rates by district
plt.title("Mortality Rates by Districts Using Bar Chart", fontsize=16, fontweight='bold')
plt.xlabel("District", fontsize=14)
plt.ylabel("Mortality Rate", fontsize=14)
plt.xticks(rotation=90, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df.can_kaybi_sayisi, kde = True, color='red')
plt.title("Distribution of the Number of Casualties by Histogram Graph", fontsize=16, fontweight='bold')
plt.xlabel("Number of Casualties", fontsize=14)                                 #Creates and displays a histogram chart visualizing the distribution of the number of casualties
plt.ylabel("Frequency", fontsize=14)
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.show()

df["can_kaybi_sayisi"].describe()  #Gives a statistical summary of the 'can_kaybi_sayisi' column

numeric_df = df.select_dtypes(include=[float, int])  #Selects numeric (float and int) columns in the data set

corr = numeric_df.corr()  #Calculates the correlation matrix between numeric columns

print(corr)  #Prints the correlation matrix on the screen

plt.figure(figsize=(16, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, linecolor='gray')   #Generates and displays heat map visualizing correlations between numerical columns
plt.title("Correlation Heat Map", fontsize=16, fontweight='bold')
plt.show()

plt.figure(figsize=(16, 6))       #Creates and displays the heatmap hiding correlation values less than 0.5
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, linecolor='gray')
plt.title("Correlation Heat Map", fontsize=16, fontweight='bold')
mask = np.zeros_like(corr)
mask[np.abs(corr) < 0.5] = True
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, linecolor='gray', mask=mask)

plt.show()

fig, ax1 = plt.subplots(figsize=(13, 6))

color = 'tab:red'
ax1.set_xlabel('District Name', fontsize=10)
ax1.set_ylabel('Number of Heavily Damaged Buildings', fontsize=10, color=color)
sns.barplot(x='ilce_adi', y='agir_hasarli_bina_sayisi', data=df, ax=ax1, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.tick_params(axis='x', rotation=90)
                                              #Constructs and displays a biaxial bar graph showing the number of severely damaged buildings and mortality rate by districts
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Mortality Rate', fontsize=10, color=color)
sns.barplot(x='ilce_adi', y='can_kaybi_sayisi', data=df, ax=ax2, alpha=0.6, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title("Bar Chart of Severely Damaged Buildings and Mortality Rate by District", fontsize=14, fontweight='bold')
fig.tight_layout()

red_patch = Patch(color='tab:red', label='Number of Heavily Damaged Buildings')
blue_patch = Patch(color='tab:blue', label='Mortality Rate')
plt.legend(handles=[red_patch, blue_patch], loc='upper left', bbox_to_anchor=(1.05, 1))

plt.show()

plt.figure(figsize=(17, 6))
sns.scatterplot(x="ilce_adi", y="can_kaybi_sayisi", color= "red", data=df)
plt.title("Scatter Plot of Mortality Rates by District", fontsize=16, fontweight= 'bold')
plt.xticks(rotation=90, fontsize=10)            #Creates and displays a scatter graph showing mortality rates by districts
plt.xlabel("Districts", fontsize=14)
plt.ylabel("Mortality Rates", fontsize=14)
plt.show()

plt.figure(figsize=(17,6))
sns.lineplot(x= "ilce_adi", y= "can_kaybi_sayisi", data = df);
plt.title("Line Plot of Mortality Rates by District", fontsize= 17, fontweight= 'bold')
plt.xticks(rotation = 90, fontsize=9)   #Creates and displays a line graph showing mortality rates by districts
plt.xlabel("Districts", fontsize= 13)
plt.ylabel("Mortality Rates", fontsize=13)
plt.show()

y = df[["can_kaybi_sayisi"]]      #Target variable for the model's properties and removes some unnecessary columns
x= df.drop(["can_kaybi_sayisi", "mahalle_koy_uavt", "ilce_adi", "mahalle_adi"], axis=1)

x_train,x_test,y_train,y_test= train_test_split(x,y, random_state=11, train_size=0.70)  #Splits features and target variables into 70% training and 30% testing

scaler = StandardScaler()      #Standardizes and scales training data / Transforms test data with the same scaling
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

rf = RandomForestRegressor(n_estimators=300, random_state=11)  #Creates a 300-tree RandomForestRegressor model and uses a fixed randomness value to control randomness

model2 = rf.fit(x_train_scaled, y_train)    #Trains the RandomForestRegressor model with scaled training data

model2.score(x_test_scaled, y_test)   #Calculates the R² (determination) score of the model on test data and evaluates how well the model performs

y_pred = rf.predict(x_test_scaled)  #Enables the model to make predictions by making predictions on test data

mse = mean_squared_error(y_test, y_pred)  #Calculate the mean squared error (MSE) between actual and predicted values
r2 = r2_score(y_test, y_pred)  #Calculates the R² (determination) score of the model

print(f"RandomForestRegressor MSE: {mse}")  #Prints the mean squared error (MSE) value on the screen
print(f"RandomForestRegressor R^2 Score: {r2}")  #Prints the R² score on the screen

feature_importances = rf.feature_importances_
features = x.columns
importance_df = pd.DataFrame({'Feature': features, 'Importance': feature_importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)
print(importance_df)

#Calculates the features of the model in order of importance and shows the most important features in order of highest to lowest importance

!pip install shap
import shap

# Define the target variable and features
target = 'can_kaybi_sayisi'
features = df.columns.difference([target, 'ilce_adi', 'mahalle_adi', 'mahalle_koy_uavt'])

X = df[features]
y = df[target]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Use SHAP to explain the model's predictions
explainer = shap.Explainer(model, X_train)
shap_values = explainer(X_test)

# Plot the feature importance
shap.summary_plot(shap_values, X_test)

lr = LinearRegression()  #Builds a simple linear regression model

model = lr.fit(x_train_scaled, y_train)  #Trains the LinearRegression model with scaled training data

model.score(x_test_scaled,y_test)   #Calculate the R² (determination) score of the model on test data and evaluate the performance of the model

model.score(x_train_scaled, y_train)  #Calculates the R² (stability) score of the model on training data, evaluates the performance of the model on training data and examines the case of overlearning

y_pred = lr.predict(x_test_scaled)  #Produces model predictions by making predictions on test data

mse = mean_squared_error(y_test, y_pred)  #Calculate the mean squared error (MSE) between actual and predicted values
r2 = r2_score(y_test, y_pred)  #Calculates the R² (determination) score of the model

print(f"LinearRegression MSE: {mse}")  #Prints the mean squared error (MSE) value on the screen
print(f"LinearRegression R^2 Score: {r2}")  #Prints the R² score on the screen

predictions_df = pd.DataFrame({'Gerçek Değerler': y_test.values, 'Tahmin Edilen Değerler': y_pred})
print(predictions_df)

residuals = y_test - y_pred
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True)
plt.title('Distribution of Model Residual Errors', fontsize=16, fontweight='bold')
plt.xlabel('Residual Errors', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.show()

#This graph shows the distribution and frequency of differences (residual errors) between model predicted values and actual values

df['toplam_hasarli_bina'] = df['cok_agir_hasarli_bina_sayisi'] + df['agir_hasarli_bina_sayisi'] + df['orta_hasarli_bina_sayisi'] + df['hafif_hasarli_bina_sayisi']
df['toplam_yarali'] = df['agir_yarali_sayisi'] + df['hafif_yarali_sayisi']
df['toplam_boru_hasari'] = df['dogalgaz_boru_hasari'] + df['icme_suyu_boru_hasari'] + df['atik_su_boru_hasari']

plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
sns.histplot(df['toplam_hasarli_bina'], kde=True, color='blue')
plt.xlabel("Total Damaged Building", fontsize= 16)
plt.title('Total Damaged Building Distribution')

plt.subplot(1, 3, 2)
sns.histplot(df['toplam_yarali'], kde=True, color='green')
plt.xlabel("Total Injured", fontsize= 16)
plt.title('Total Injured Distribution')

plt.subplot(1, 3, 3)
sns.histplot(df['toplam_boru_hasari'], kde=True, color='red')
plt.xlabel("Total Pipe Damage", fontsize= 16)
plt.title('Total Pipe Damage Distribution')

plt.tight_layout()
plt.show()

#Creates and displays three histogram plots showing the distribution of total damaged buildings, total injured and total pipe damage

df_grouped = df.groupby('ilce_adi').agg({
    'toplam_hasarli_bina': 'sum',
    'toplam_yarali': 'sum',
    'toplam_boru_hasari': 'sum'
}).reset_index()

plt.figure(figsize=(18, 7))

plt.subplot(1, 3, 1)
sns.barplot(x='ilce_adi', y='toplam_hasarli_bina', data=df_grouped, palette='viridis')
plt.xticks(rotation=90)
plt.xlabel("District", fontsize=16)
plt.ylabel("Total Damaged Building", fontsize=16)
plt.title('Total Damaged Buildings by Districts', fontsize=18)

plt.subplot(1, 3, 2)
sns.barplot(x='ilce_adi', y='toplam_yarali', data=df_grouped, palette='viridis')
plt.xticks(rotation=90)
plt.xlabel("District", fontsize=16)
plt.ylabel("Total Injured", fontsize=16)
plt.title('Total Injured by District', fontsize=18)

plt.subplot(1, 3, 3)
sns.barplot(x='ilce_adi', y='toplam_boru_hasari', data=df_grouped, palette='viridis')
plt.xticks(rotation=90)
plt.xlabel("District", fontsize=16)
plt.ylabel("Total Pipe Damage", fontsize=16)
plt.title('Total Pipe Damage by Districts', fontsize=18)

plt.tight_layout()
plt.show()

#Creates and displays three bar charts showing total damaged buildings, total injured and total pipe damage by district

import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth

# Coğrafi veri setini yükleme
geo_data_url = 'https://raw.githubusercontent.com/ozanyerli/istanbul-districts-geojson/main/istanbul-districts.json'
geo_data = gpd.read_file(geo_data_url)

# IBB verilerini yükleme
ib_data = pd.read_csv("deprem.csv", encoding="ISO-8859-9", delimiter=";")
ib_data['risk_seviyesi'] = ib_data['can_kaybi_sayisi']

# GeoDataFrame ile Pandas DataFrame'i birleştirme
geo_data = geo_data.merge(ib_data, left_on='name', right_on='ilce_adi')

# Harita oluşturma
m = folium.Map(location=[41.0082, 28.9784], zoom_start=11)

# Risk seviyelerini haritada gösterme
Choropleth(
    geo_data=geo_data,
    data=geo_data,
    columns=['ilce_adi', 'risk_seviyesi'],
    key_on='feature.properties.ilce_adi',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Risk Seviyesi'
).add_to(m)

# Haritayı kaydetme
m.save('/content/istanbul_risk_haritasi.html')

from folium import Html

# Create HTML with the map
html = Html("""<iframe src="/content/istanbul_risk_haritasi.html" width="800" height="600"></iframe>""", script=True)

# Add HTML to the map
m.add_child(html)

# Display the map (might not render perfectly)
m

import shap

explainer = shap.Explainer(model, X_train_scaled)
shap_values = explainer(X_test_scaled)

shap.summary_plot(shap_values, X_test_scaled, feature_names=X.columns)

import numpy as np
import pandas as pd
from scipy.linalg import pinv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import time
import os

def hardlim(x):
    return np.where(x >= 0, 1, 0)

def tribas(x):
    return np.maximum(1 - np.abs(x), 0)

def radbas(x):
    return np.exp(-np.power(x, 2))

def CELM(TrainingData_File, TestingData_File, NumberofHiddenNeurons, ActivationFunction, C):
    # Load training dataset
    train_data = np.loadtxt(TrainingData_File)
    T = train_data[:, 0].T
    P = train_data[:, 1:].T
    # Load testing dataset
    test_data = np.loadtxt(TestingData_File)
    TV_T = test_data[:, 0].T
    TV_P = test_data[:, 1:].T
    NumberofTrainingData = P.shape[1]
    NumberofTestingData = TV_P.shape[1]
    NumberofInputNeurons = P.shape[0]

    # Calculate weights & biases
    start_time_train = time.time()

    InputWeight = np.random.rand(NumberofHiddenNeurons, NumberofInputNeurons) * 2 - 1
    BiasofHiddenNeurons = np.random.rand(NumberofHiddenNeurons, 1)

    tempH = np.dot(InputWeight, P) + BiasofHiddenNeurons

    # Calculate hidden neuron output matrix H
    if ActivationFunction in ['sig', 'sigmoid']:
        H = 1 / (1 + np.exp(-tempH))
    elif ActivationFunction == 'sin':
        H = np.sin(tempH)
    elif ActivationFunction == 'hardlim':
        H = hardlim(tempH)
    elif ActivationFunction == 'tribas':
        H = tribas(tempH)
    elif ActivationFunction == 'radbas':
        H = radbas(tempH)

    if C == 10 ** 100:
        OutputWeight = np.dot(pinv(H.T), T.T)
    else:
        OutputWeight = np.linalg.solve(np.eye(H.shape[0]) / C + np.dot(H, H.T), np.dot(H, T.T))

    end_time_train = time.time()
    TrainingTime = end_time_train - start_time_train

    # Calculate the training accuracy
    Y = np.dot(H.T, OutputWeight).T
    TrainingRMSE = np.sqrt(np.mean(np.square(T - Y)))
    TrainingMAE = np.mean(np.abs(T - Y))
    TrainingMSE = mean_squared_error(T, Y)
    TrainingR2 = r2_score(T, Y)

    # Calculate the output of testing input
    start_time_test = time.time()
    tempH_test = np.dot(InputWeight, TV_P) + BiasofHiddenNeurons
    if ActivationFunction in ['sig', 'sigmoid']:
        H_test = 1 / (1 + np.exp(-tempH_test))
    elif ActivationFunction == 'sin':
        H_test = np.sin(tempH_test)
    elif ActivationFunction == 'hardlim':
        H_test = hardlim(tempH_test)
    elif ActivationFunction == 'tribas':
        H_test = tribas(tempH_test)
    elif ActivationFunction == 'radbas':
        H_test = radbas(tempH_test)
    TY = np.dot(H_test.T, OutputWeight).T
    end_time_test = time.time()
    TestingTime = end_time_test - start_time_test
    TestingRMSE = np.sqrt(np.mean(np.square(TV_T - TY)))
    TestingMAE = np.mean(np.abs(TV_T - TY))
    TestingMSE = mean_squared_error(TV_T, TY)
    TestingR2 = r2_score(TV_T, TY)

    return TrainingTime, TestingTime, TrainingRMSE, TestingRMSE, TrainingMAE, TestingMAE, TrainingMSE, TestingMSE, TrainingR2, TestingR2

# Veri setini yükle
data = pd.read_csv("deprem.csv", encoding="ISO-8859-9", delimiter=";")

# Özellikler ve hedef değişkeni ayır
X = data.drop(['ilce_adi', 'mahalle_adi', 'mahalle_koy_uavt', 'can_kaybi_sayisi', 'atik_su_boru_hasari','icme_suyu_boru_hasari','dogalgaz_boru_hasari'], axis=1)
y = data['can_kaybi_sayisi']

# Veriyi ölçeklendir
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Veri setini eğitim ve test olarak böl
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Hiperparametre optimizasyonu ve farklı aktivasyon fonksiyonları için döngü
activation_functions = ['sig', 'sin', 'hardlim', 'tribas', 'radbas']
neurons_list = [100, 200, 500, 1000, 2000,5000]
c_list = [10, 100, 1000, 10000, 100000,10**12]

# Sonuçları saklamak için bir liste oluştur
results_list = []

for act_func in activation_functions:
    for neurons in neurons_list:
        for c in c_list:
            # Verileri CELM'in beklediği formata dönüştür
            train_data = np.column_stack((y_train, X_train))
            test_data = np.column_stack((y_test, X_test))

            # Geçici dosyalar oluştur
            np.savetxt('temp_train.txt', train_data)
            np.savetxt('temp_test.txt', test_data)

            # CELM modelini çalıştır
            TrainingTime, TestingTime, TrainingRMSE, TestingRMSE, TrainingMAE, TestingMAE, TrainingMSE, TestingMSE, TrainingR2, TestingR2 = CELM(
                'temp_train.txt',
                'temp_test.txt',
                NumberofHiddenNeurons=neurons,
                ActivationFunction=act_func,
                C=c
            )

            # Sonuçları listeye ekle
            results_list.append({
                'Activation': act_func,
                'Neurons': neurons,
                'C': c,
                'Train Time': TrainingTime,
                'Test Time': TestingTime,
                'Train RMSE': TrainingRMSE,
                'Test RMSE': TestingRMSE,
                'Train MAE': TrainingMAE,
                'Test MAE': TestingMAE,
                'Train MSE': TrainingMSE,
                'Test MSE': TestingMSE,
                'Train R²': TrainingR2,
                'Test R²': TestingR2
            })

            # Geçici dosyaları sil
            os.remove('temp_train.txt')
            os.remove('temp_test.txt')

# Sonuçları DataFrame'e dönüştür
results = pd.DataFrame(results_list)

# Sonuçları göster
print(results.to_string(index=False))

# En iyi Test RMSE, Test MAE, Test MSE ve Test R² sonuçlarını bul
best_rmse = results['Test RMSE'].min()
best_mae = results['Test MAE'].min()
best_mse = results['Test MSE'].min()
best_rkare = results['Test R²'].max()

print("\nEn iyi Test RMSE:")
print(results[results['Test RMSE'] == best_rmse][['Activation', 'Neurons', 'C', 'Test RMSE']].to_string(index=False))

print("\nEn iyi Test MAE:")
print(results[results['Test MAE'] == best_mae][['Activation', 'Neurons', 'C', 'Test MAE']].to_string(index=False))

print("\nEn iyi Test MSE:")
print(results[results['Test MSE'] == best_mse][['Activation', 'Neurons', 'C', 'Test MSE']].to_string(index=False))

print("\nEn iyi Test R²:")
print(results[results['Test R²'] == best_rkare][['Activation', 'Neurons', 'C', 'Test R²']].to_string(index=False))

import numpy as np
import pandas as pd
from scipy.linalg import pinv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import time
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def hardlim(x):
    return np.where(x >= 0, 1, 0)

def tribas(x):
    return np.maximum(1 - np.abs(x), 0)

def radbas(x):
    return np.exp(-np.power(x, 2))

def CELM(TrainingData_File, TestingData_File, NumberofHiddenNeurons, ActivationFunction, C):
    # Load training dataset
    train_data = np.loadtxt(TrainingData_File)
    T = train_data[:, 0].T
    P = train_data[:, 1:].T
    # Load testing dataset
    test_data = np.loadtxt(TestingData_File)
    TV_T = test_data[:, 0].T
    TV_P = test_data[:, 1:].T
    NumberofTrainingData = P.shape[1]
    NumberofTestingData = TV_P.shape[1]
    NumberofInputNeurons = P.shape[0]

    # Calculate weights & biases
    start_time_train = time.time()

    InputWeight = np.random.rand(NumberofHiddenNeurons, NumberofInputNeurons) * 2 - 1
    BiasofHiddenNeurons = np.random.rand(NumberofHiddenNeurons, 1)

    tempH = np.dot(InputWeight, P) + BiasofHiddenNeurons

    # Calculate hidden neuron output matrix H
    if ActivationFunction in ['sig', 'sigmoid']:
        H = 1 / (1 + np.exp(-tempH))
    elif ActivationFunction == 'sin':
        H = np.sin(tempH)
    elif ActivationFunction == 'hardlim':
        H = hardlim(tempH)
    elif ActivationFunction == 'tribas':
        H = tribas(tempH)
    elif ActivationFunction == 'radbas':
        H = radbas(tempH)

    if C == 10 ** 100:
        OutputWeight = np.dot(pinv(H.T), T.T)
    else:
        OutputWeight = np.linalg.solve(np.eye(H.shape[0]) / C + np.dot(H, H.T), np.dot(H, T.T))

    end_time_train = time.time()
    TrainingTime = end_time_train - start_time_train

    # Calculate the training accuracy
    Y = np.dot(H.T, OutputWeight).T
    TrainingRMSE = np.sqrt(np.mean(np.square(T - Y)))
    TrainingMAE = np.mean(np.abs(T - Y))
    TrainingMSE = np.mean(np.square(T - Y))
    TrainingR2 = r2_score(T, Y)

    # Calculate the output of testing input
    start_time_test = time.time()
    tempH_test = np.dot(InputWeight, TV_P) + BiasofHiddenNeurons
    if ActivationFunction in ['sig', 'sigmoid']:
        H_test = 1 / (1 + np.exp(-tempH_test))
    elif ActivationFunction == 'sin':
        H_test = np.sin(tempH_test)
    elif ActivationFunction == 'hardlim':
        H_test = hardlim(tempH_test)
    elif ActivationFunction == 'tribas':
        H_test = tribas(tempH_test)
    elif ActivationFunction == 'radbas':
        H_test = radbas(tempH_test)
    TY = np.dot(H_test.T, OutputWeight).T
    end_time_test = time.time()
    TestingTime = end_time_test - start_time_test
    TestingRMSE = np.sqrt(np.mean(np.square(TV_T - TY)))
    TestingMAE = np.mean(np.abs(TV_T - TY))
    TestingMSE = np.mean(np.square(TV_T - TY))
    TestingR2 = r2_score(TV_T, TY)

    return TrainingTime, TestingTime, TrainingRMSE, TestingRMSE, TrainingMAE, TestingMAE, TrainingMSE, TestingMSE, TrainingR2, TestingR2

# Veri setini yükle
data = pd.read_csv("deprem.csv", encoding="ISO-8859-9", delimiter=";")

# Özellikler ve hedef değişkeni ayır shap ile işe yaramayan featureları drop et
## X = data.drop(['ilce_adi', 'mahalle_adi', 'mahalle_koy_uavt', 'can_kaybi_sayisi'], axis=1)
X = data.drop(['ilce_adi', 'mahalle_adi', 'mahalle_koy_uavt', 'can_kaybi_sayisi', 'atik_su_boru_hasari','icme_suyu_boru_hasari','dogalgaz_boru_hasari'], axis=1)
y = data['can_kaybi_sayisi']

# Veriyi ölçeklendir
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Veri setini eğitim ve test olarak böl
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Hiperparametre optimizasyonu ve farklı aktivasyon fonksiyonları için döngü
activation_functions = ['sig', 'sin', 'hardlim', 'tribas', 'radbas']
neurons_list = [100, 200, 500, 1000, 2000, 5000]
c_list = [10, 100, 1000, 10000, 100000, 10**10]

# Sonuçları saklamak için bir liste oluştur
results_list = []

for act_func in activation_functions:
    for neurons in neurons_list:
        for c in c_list:
            # Verileri CELM'in beklediği formata dönüştür
            train_data = np.column_stack((y_train, X_train))
            test_data = np.column_stack((y_test, X_test))

            # Geçici dosyalar oluştur
            np.savetxt('temp_train.txt', train_data)
            np.savetxt('temp_test.txt', test_data)

            # CELM modelini çalıştır
            TrainingTime, TestingTime, TrainingRMSE, TestingRMSE, TrainingMAE, TestingMAE, TrainingMSE, TestingMSE, TrainingR2, TestingR2 = CELM(
                'temp_train.txt',
                'temp_test.txt',
                NumberofHiddenNeurons=neurons,
                ActivationFunction=act_func,
                C=c
            )

            # Sonuçları listeye ekle
            results_list.append({
                'Activation': act_func,
                'Neurons': neurons,
                'C': c,
                'Train Time': TrainingTime,
                'Test Time': TestingTime,
                'Train RMSE': TrainingRMSE,
                'Test RMSE': TestingRMSE,
                'Train MAE': TrainingMAE,
                'Test MAE': TestingMAE,
                'Train MSE': TrainingMSE,
                'Test MSE': TestingMSE,
                'Train R²': TrainingR2,
                'Test R²': TestingR2
            })

            # Geçici dosyaları sil
            os.remove('temp_train.txt')
            os.remove('temp_test.txt')

# Sonuçları DataFrame'e dönüştür
results = pd.DataFrame(results_list)

# En iyi Test RMSE, Test MAE ve Test R² sonuçlarını bul
best_rmse = results['Test RMSE'].min()
best_mae = results['Test MAE'].min()
best_mse = results['Test MSE'].min()
best_rkare = results['Test R²'].max()

# En iyi sonuçları seç
best_rmse_row = results[results['Test RMSE'] == best_rmse]
best_mae_row = results[results['Test MAE'] == best_mae]
best_mse_row = results[results['Test MSE'] == best_mse]
best_r2_row = results[results['Test R²'] == best_rkare]

# En iyi aktivasyon fonksiyonlarını bul
best_rmse_activation = best_rmse_row['Activation'].values[0]
best_mae_activation = best_mae_row['Activation'].values[0]
best_mse_activation = best_mse_row['Activation'].values[0]
best_r2_activation = best_r2_row['Activation'].values[0]

# En iyi değerlerin koordinatlarını belirle
best_rmse_coords = (best_rmse_row['Neurons'].values[0], best_rmse_row['C'].values[0])
best_mae_coords = (best_mae_row['Neurons'].values[0], best_mae_row['C'].values[0])
best_mse_coords = (best_mse_row['Neurons'].values[0], best_mse_row['C'].values[0])
best_r2_coords = (best_r2_row['Neurons'].values[0], best_r2_row['C'].values[0])

# Meshgrid oluştur
neurons_list = np.array(neurons_list)
c_list = np.array(c_list)
N, C = np.meshgrid(neurons_list, c_list)

# RMSE, MAE, MSE ve R² Matrislerini Doldur
RMSE = np.zeros((len(c_list), len(neurons_list)))
MAE = np.zeros((len(c_list), len(neurons_list)))
MSE = np.zeros((len(c_list), len(neurons_list)))
R2 = np.zeros((len(c_list), len(neurons_list)))

for idx, c in enumerate(c_list):
    for jdx, neurons in enumerate(neurons_list):
        filtered_result = results[(results['Neurons'] == neurons) & (results['C'] == c)]
        if not filtered_result.empty:
            RMSE[idx, jdx] = filtered_result['Test RMSE'].values[0]
            MAE[idx, jdx] = filtered_result['Test MAE'].values[0]
            MSE[idx, jdx] = filtered_result['Test MSE'].values[0]
            R2[idx, jdx] = filtered_result['Test R²'].values[0]
        else:
            RMSE[idx, jdx] = np.nan
            MAE[idx, jdx] = np.nan
            MSE[idx, jdx] = np.nan
            R2[idx, jdx] = np.nan

# Grafiklerin oluşturulması
fig = plt.figure(figsize=(18, 6))


# MSE Plot
ax1 = fig.add_subplot(131, projection='3d')
surf1 = ax1.plot_surface(N, C, MSE, cmap='viridis', edgecolor='none')
ax1.scatter(best_mse_coords[0], best_mse_coords[1], best_mse, color='r', s=50,
            label=f'Best MSE: {best_mse:.4f} ({best_mse_activation})')
ax1.set_xlabel('Number of Neurons')
ax1.set_ylabel('C (Regularization Parameter)')
ax1.set_zlabel('Test MSE')
ax1.set_title('MSE Surface Plot')
ax1.legend()

# RMSE Plot
##ax2 = fig.add_subplot(142, projection='3d')
##surf2 = ax2.plot_surface(N, C, RMSE, cmap='coolwarm', edgecolor='none', vmin=RMSE.min(), vmax=RMSE.max())
##ax2.scatter(best_rmse_coords[0], best_rmse_coords[1], best_rmse, color='r', s=50,
##            label=f'Best RMSE: {best_rmse:.4f} ({best_rmse_activation})')
##ax2.set_xlabel('Number of Neurons')
##ax2.set_ylabel('C (Regularization Parameter)')
##ax2.set_zlabel('Test RMSE')
##ax2.set_title('RMSE Surface Plot')
##ax2.legend()

# MAE Plot
ax2 = fig.add_subplot(132, projection='3d')
surf2 = ax2.plot_surface(N, C, MAE, cmap='coolwarm', edgecolor='none', vmin=MAE.min(), vmax=MAE.max())
ax2.scatter(best_mae_coords[0], best_mae_coords[1], best_mae, color='r', s=50,
            label=f'Best MAE: {best_mae:.4f} ({best_mae_activation})')
ax2.set_xlabel('Number of Neurons')
ax2.set_ylabel('C (Regularization Parameter)')
ax2.set_zlabel('Test MAE')
ax2.set_title('MAE Surface Plot')
ax2.legend()



# R² Plot
ax3 = fig.add_subplot(133, projection='3d')
surf3 = ax3.plot_surface(N, C, R2, cmap='coolwarm', edgecolor='none', vmin=R2.min(), vmax=R2.max())
ax3.scatter(best_r2_coords[0], best_r2_coords[1], best_rkare, color='b', s=50,
            label=f'Best R²: {best_rkare:.4f} ({best_r2_activation})')
ax3.set_xlabel('Number of Neurons')
ax3.set_ylabel('C (Regularization Parameter)')
ax3.set_zlabel('Test R²')
ax3.set_title('R² Surface Plot')
ax3.legend()

plt.tight_layout()
plt.show()

from sklearn.feature_selection import mutual_info_regression

mi = mutual_info_regression(x, y)

# Özellikleri ve mutual bilgi değerleri DataFrame ile birleştirilir
mi_df = pd.DataFrame({'Özellik': x.columns, 'Mutual Bilgi': mi})
mi_df = mi_df.sort_values(by='Mutual Bilgi', ascending=False)

# En yüksek mutual bilgiye sahip özellik seçilir
selected_features = mi_df.head(10)['Özellik'].tolist()
print("Seçilen Özellikler:", selected_features)

# Seçilen özelliklerle veri seti hazırlanır
X_selected = X[selected_features]

X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=300, random_state=42)
model = rf.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RandomForestRegressor MSE: {mse}")
print(f"RandomForestRegressor R^2 Score: {r2}")

# Özelliklerin önem derecelerini görüntülemek
feature_importances = rf.feature_importances_
importance_df = pd.DataFrame({'Özellik': selected_features, 'Önemi': feature_importances})
importance_df = importance_df.sort_values(by='Önemi', ascending=False)
print(importance_df)

!pip install catboost

# CatBoostRegressor Modeli
start_time_catboost = time.time()  # Başlangıç zamanını al
categorical_features = ['ilce_adi', 'mahalle_adi']

catboost_model = CatBoostRegressor(iterations=300, depth=6, learning_rate=0.1, loss_function='RMSE', cat_features=categorical_features, verbose=0)
catboost_model.fit(X_train, y_train)
end_time_catboost = time.time()  # Bitiş zamanını al

y_pred_catboost = catboost_model.predict(x_test)

mse_catboost = mean_squared_error(y_test, y_pred_catboost)
r2_catboost = r2_score(y_test, y_pred_catboost)
catboost_time = end_time_catboost - start_time_catboost  # Süreyi hesapla

print(f"CatBoostRegressor MSE: {mse_catboost}")
print(f"CatBoostRegressor R^2 Score: {r2_catboost}")
print(f"CatBoostRegressor Süre: {catboost_time} saniye")

from sklearn.svm import SVR
import time

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

svm_model = SVR(kernel='rbf', C=100, gamma='scale')  # Kernel ve hiperparametreleri ihtiyacınıza göre ayarlayın
svm_model.fit(X_train, y_train)

start_time_svm = time.time()  # Eğitim süresi başlangıcı
svm_model = SVR(kernel='rbf', C=100, gamma='scale')  # Kernel ve hiperparametreleri ihtiyacınıza göre ayarlayın
svm_model.fit(X_train, y_train)
end_time_svm = time.time()  # Eğitim süresi bitişi

y_pred_svm = svm_model.predict(X_test)

mse_svm = mean_squared_error(y_test, y_pred_svm)
r2_svm = r2_score(y_test, y_pred_svm)

svm_time = end_time_svm - start_time_svm

print(f"SVR MSE: {mse_svm}")
print(f"SVR R^2 Score: {r2_svm}")
print(f"SVR Eğitim Süresi: {svm_time:.2f} saniye")

!pip install mrmr_selection

from mrmr import mrmr_classif

K = 10
selected_features = mrmr_classif(X, y, K)

print("Seçilen Özellikler:", selected_features)

selected_df = df[selected_features + ['can_kaybi_sayisi']]

X_train, X_test, y_train, y_test = train_test_split(
    selected_df.drop('can_kaybi_sayisi', axis=1),
    selected_df['can_kaybi_sayisi'],
    test_size=0.2,
    random_state=42
)


start_time = time.time()  # Başlangıç zamanını al
model = RandomForestRegressor()
model.fit(X_train, y_train)
end_time = time.time()  # Bitiş zamanını al


model = RandomForestRegressor()
model.fit(X_train, y_train)

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
training_time = end_time - start_time

print(f"Mean Squared Error (MSE): {mse}")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R-squared (R²): {r2}")
print(f"Model Eğitim Süresi: {training_time} saniye")

!pip install xgboost

!pip install shap

import xgboost as xgb
import shap
import time

start_time = time.time()

bagımlı = 'can_kaybi_sayisi'
bagımsız = df.columns.difference([target, 'ilce_adi', 'mahalle_adi', 'mahalle_koy_uavt'])

X = df[bagımsız]
y = df[bagımlı]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

preprocessing_time = time.time() - start_time
print(f"Data preprocessing time: {preprocessing_time:.2f} seconds")
start_time = time.time()

xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
xgb_model.fit(X_train_scaled, y_train)

training_time = time.time() - start_time
print(f"XGBoost training time: {training_time:.2f} seconds")

start_time = time.time()

y_pred_xgb = xgb_model.predict(X_test_scaled)

prediction_time = time.time() - start_time
print(f"XGBoost prediction time: {prediction_time:.2f} seconds")

mse_xgb = mean_squared_error(y_test, y_pred_xgb)
r2_xgb = r2_score(y_test, y_pred_xgb)

print(f"XGBoost MSE: {mse_xgb}")
print(f"XGBoost R^2 Score: {r2_xgb}")

start_time = time.time()

explainer_xgb = shap.Explainer(xgb_model, X_train_scaled)
shap_values_xgb = explainer_xgb(X_test_scaled)

shap_time = time.time() - start_time
print(f"SHAP analysis time: {shap_time:.2f} seconds")

shap.summary_plot(shap_values_xgb, X_test_scaled)

from sklearn.model_selection import GridSearchCV

start_time = time.time()

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 6, 10],
    'learning_rate': [0.01, 0.1, 0.2]
}

grid_search = GridSearchCV(estimator=xgb.XGBRegressor(objective='reg:squarederror', random_state=42),
                           param_grid=param_grid, scoring='neg_mean_squared_error', cv=3, verbose=1)
grid_search.fit(X_train_scaled, y_train)

tuning_time = time.time() - start_time
print(f"GridSearchCV hyperparameter tuning time: {tuning_time:.2f} seconds")

best_xgb_model = grid_search.best_estimator_
best_y_pred_xgb = best_xgb_model.predict(X_test_scaled)

best_mse_xgb = mean_squared_error(y_test, best_y_pred_xgb)
best_r2_xgb = r2_score(y_test, best_y_pred_xgb)

print(f"Best XGBoost MSE with GridSearchCV: {best_mse_xgb}")
print(f"Best XGBoost R^2 Score with GridSearchCV: {best_r2_xgb}")
