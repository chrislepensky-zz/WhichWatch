from pyimage.pipeline import ImagePipeline
from sklearn.preprocessing import StandardScaler
from skimage.color import rgb2gray
from skimage.feature import canny
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from skimage.filters import sobel
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from lasagne import layers
from lasagne.nonlinearities import  softmax, rectify
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet
from pyimage import ImagePipeline
import numpy as np
import pickle
import cPickle

#directory = '/Volumes/MacintoshHD/Users/Chris/Desktop/images/data'
def pipeline(directory):
	pipe = ImagePipeline(directory)
	pipe.read(sub_dirs=('casual', 'dress'))
	pipe.resize((300, 300, 3))
	#pipe.transform(rgb2gray, {})
	pipe.vectorize()
	return pipe

def random_forest(pipe):
	X_train, X_test, y_train, y_test = train_test_split(pipe.features, pipe.labels)
	rf = RandomForestClassifier(n_estimators=500, n_jobs=-1)
	rf.fit(X_train, y_train)
	y_predict = rf.predict(X_test)

	print "precision for random forest:", precision_score(y_test, y_predict)
	print "recall for random forest:", recall_score(y_test, y_predict)
	print "f1 for random forest:", f1_score(y_test, y_predict, average='weighted')


def svm(pipe):
	X_train, X_test, y_train, y_test = train_test_split(pipe.features, pipe.labels)
	svm = SVC(kernel='linear')
	svm.fit(X_train, y_train)
	y_predict = svm.predict(X_test)

	print "precision for svm:", precision_score(y_test, y_predict)
	print "recall for svm:", recall_score(y_test, y_predict)
	print "f1 for svm:", f1_score(y_test, y_predict, average='weighted')


def knn(pipe):
	X_train, X_test, y_train, y_test = train_test_split(pipe.features, pipe.labels)
	knn = KNeighborsClassifier()
	knn.fit(X_train, y_train)
	y_predict = knn.predict(X_test)

	print "precision for knn:", precision_score(y_test, y_predict)
	print "recall for knn:", recall_score(y_test, y_predict)
	print "f1 for knn:", f1_score(y_test, y_predict, average='weighted')
	#pickle.dump( knn, open( "model.p", "wb" ) )

def nnet(pipe):
	pipe.features = pipe.features.astype(np.float32)
	pipe.labels = pipe.labels.astype(np.int32)
	pipe.features = StandardScaler().fit_transform(pipe.features)
	X_train, X_test, y_train, y_test = train_test_split(pipe.features, pipe.labels)
	nnet = NeuralNet(
	          # Specify the layers
	          layers=[('input', layers.InputLayer),
	                  ('hidden1', layers.DenseLayer),
	                  ('hidden2', layers.DenseLayer),
	                  ('hidden3', layers.DenseLayer),
	                  ('output', layers.DenseLayer)],

	          # Input Layer
	          input_shape=(None, pipe.features.shape[1]),

	          # Hidden Layer 1
	          hidden1_num_units=512,
	          hidden1_nonlinearity=rectify,

	          # Hidden Layer 2
	          hidden2_num_units=512,
	          hidden2_nonlinearity=rectify,

	          # # Hidden Layer 3
	          hidden3_num_units=512,
	          hidden3_nonlinearity=rectify,

	          # Output Layer
	          output_num_units=2,
	          output_nonlinearity=softmax,

	          # Optimization
	          update=nesterov_momentum,
	          update_learning_rate=0.001,
	          update_momentum=0.3,
	          max_epochs=30,

	          # Others,
	          regression=False,
	          verbose=1,
	   		)
	         
	nnet.fit(X_train, y_train)
	y_predict = nnet.predict(X_test)

	print "precision for nnet:", precision_score(y_test, y_predict)
	print "recall for nnet:", recall_score(y_test, y_predict)
	print "f1 for nnet:", f1_score(y_test, y_predict, average='weighted')
	pickle.dump( nnet, open( "model.pkl", "wb" ), protocol = cPickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
	pipe = pipeline('/Volumes/MacintoshHD/Users/Chris/Desktop/images/data')
	nnet(pipe)
