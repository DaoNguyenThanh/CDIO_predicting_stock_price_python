from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename


#Đọc file
Tk().withdraw()
file= askopenfilename()
df = pd.read_csv(file)                          

#Tạo list ngày
dates = list(range(0,int(len(df))))                                             
prices = df['Close']
#Xoá bỏ các dữ liệu không phải là số
prices[np.isnan(prices)] = np.median(prices[~np.isnan(prices)])                 

#Chuyển số liệu thành ma trận
dates = np.asanyarray(dates)
prices = np.asanyarray(prices)
dates = np.reshape(dates,(len(dates),1))
prices = np.reshape(prices, (len(prices), 1))

#Lấy độ chính xác của mô hình trước
try:
  pickle_in = open("prediction.pickle", "rb")
  reg = pickle.load(pickle_in)
  xtrain, xtest, ytrain, ytest = train_test_split(dates, prices, test_size=0.2)
  best = reg.score(ytrain, ytest)
except:
  pass

#Chọn mô hình chuẩn xác nhất
best = 0
for _ in range(100):
    xtrain, xtest, ytrain, ytest = train_test_split(dates, prices, test_size=0.2)
    reg = LinearRegression().fit(xtrain, ytrain)
    acc = reg.score(xtest, ytest)
    if acc > best:
        best = acc
        #Lưu độ chính xác của mô hình
        with open('prediction.pickle','wb') as f:
            pickle.dump(reg, f)
        print(acc)
        
#Load linear regression model
pickle_in = open("prediction.pickle", "rb")
reg = pickle.load(pickle_in)

#Lấy độ chính xác trung bình của mô hình
mean = 0
for i in range(10):
  #Random Split Data
  msk = np.random.rand(len(df)) < 0.8
  xtest = dates[~msk]
  ytest = prices[~msk]
  mean += reg.score(xtest,ytest)

print("Average Accuracy:", mean/10)

#Plot Predicted VS Actual Data
plt.plot(xtest, ytest, color='green',linewidth=1, label= 'Actual Price')                        
plt.plot(xtest, reg.predict(xtest), color='blue', linewidth=3, label = 'Predicted Price')       
plt.title('Linear Regression | Time vs. Price ')
plt.legend()
plt.xlabel('Date Integer')
plt.show()

#
from sklearn.metrics import r2_score
print("Giá trị R: ", r2_score(ytest, reg.predict(xtest)))

