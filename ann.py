import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from price import GetData
def main():
    X,Y = GetData('BTCUSDT','15m', '5 day ago UTC', 89)
    labelencoder_X_4 = LabelEncoder()
    X[:, 4] = labelencoder_X_4.fit_transform(X[:, 4])
    transformer = ColumnTransformer(
    transformers=[
        ("OneHot",        # Just a name
         OneHotEncoder(), # The transformer class
         [5]              # The column(s) to be applied on.
         )
    ],
    remainder='passthrough' # donot apply anything to the remaining columns
    )
    X = transformer.fit_transform(X.tolist())
    X = X.astype('float64')
    # 預防虛擬變量陷阱
    #X = X[:,1:]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
main()