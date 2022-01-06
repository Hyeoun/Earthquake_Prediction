import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import Adam
import glob
from tensorflow.keras.callbacks import EarlyStopping

data_paths = glob.glob('./datasets/location_pre/*')
te = 100
for i in data_paths:
    temp = (i.split('(')[1]).split(')')[0]

    try:
        X_train, X_test, Y_train, Y_test = np.load(i, allow_pickle=True)

        model = Sequential()
        model.add(LSTM(128, input_shape = (te, 6), activation = 'tanh'))
        model.add(Dropout(0.2))
        model.add(Dense(64, activation='tanh'))
        model.add(Dropout(0.1))
        model.add(Dense(32, activation='tanh'))
        model.add(Dropout(0.05))
        model.add(Flatten())

        model.add(Dense(6))  # 값을 출력할때는 출력에 활성화 함수를 넣지 않는다.
        early_stopping = EarlyStopping(monitor='val_loss', patience=7)
        model.compile(loss = 'mse', optimizer = 'adam')
        model.summary()

        fit_hist = model.fit(X_train, Y_train, epochs=50, validation_data=(X_test, Y_test), shuffle = False, callbacks=[early_stopping], verbose=1)
        if temp == 'X_120~150,Y_30~60':
            plt.plot(fit_hist.history['loss'][-500:], label = 'loss')
            plt.plot(fit_hist.history['val_loss'][-500:], label = 'val_loss')
            plt.legend()
            plt.show()

            predict = model.predict(X_test)
            print(predict[-10:, 1], predict[-10:, 0])
            print(Y_test[-10:, 1], Y_test[-10:, 0])

            fig = plt.figure(figsize=(9,5))
            ax = fig.add_axes([0,0,1,1])  # 전체 figure 전부 활용
            ax.plot(Y_test[-10:, 1], Y_test[-10:, 0], '.', markersize=5, alpha=0.7, color='b')
            ax.plot(predict[-10:, 1], predict[-10:, 0], '.', markersize=5, alpha=1, color='#ff5555')
            plt.show()

            plt.plot(Y_test[-10:, 3], label = 'actual')
            plt.plot(predict[-10:, 3], label = 'predict')
            plt.legend()
            plt.show()
    except:
        print(temp)

    model.save('./models/earthquake_pred_{}.h5'.format(temp))