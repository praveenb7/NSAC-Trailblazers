import pickle
import numpy as np

model = pickle.load(open('model.pkl', 'rb'))
int_features=[30, 50, 10]     # [oxygen, temperature, humidity]
final = [np.array(int_features)]
prediction=model.predict_proba(final)
output = '{0:.{1}f}'.format(prediction[0][1], 2)

print(output)