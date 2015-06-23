from pyimage.pipeline import ImagePipeline
from skimage.color import rgb2gray
from skimage.feature import canny
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from skimage.filters import sobel
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from pyimage import ImagePipeline
import pickle

#directory = '/Volumes/MacintoshHD/Users/Chris/Desktop/images/data'
def pipeline(directory):
	pipe = ImagePipeline(directory)
	pipe.read(sub_dirs=('casual', 'dress'))
	pipe.resize((300, 300, 3))
	pipe.transform(rgb2gray, {})
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
	pickle.dump( knn, open( "model.p", "wb" ) )

if __name__ == '__main__':
	pipe = pipeline('/Volumes/MacintoshHD/Users/Chris/Desktop/images/data')
	knn(pipe)
