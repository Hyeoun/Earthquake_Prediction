import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import Adam

loc = './datasets/earthquake_preprocessed_(X_136~148,Y_32~43,T_300).npy'
te = loc.split('T_')
te = int((te[1].split(')'))[0])

X_train, X_test, Y_train, Y_test = np.load(loc, allow_pickle=True)

model = Sequential()
model.add(LSTM(128, input_shape = (te, 6), activation = 'tanh'))
model.add(Flatten())


model.add(Dense(6))  # 값을 예측할때는 출력에 활성화 함수를 넣지 않는다.
model.compile(loss = 'mse', optimizer = 'adam')
model.summary()

fit_hist = model.fit(X_train, Y_train, epochs=10, validation_data=(X_test, Y_test), shuffle = False, verbose=1)

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

model.save('./models/earthquake_pred_{}.h5'.format(fit_hist.history['val_loss'][-1]))