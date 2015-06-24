from skimage import io
from skimage.transform import resize
from pyimage.pipeline import ImagePipeline
from skimage.color import rgb2gray
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import numpy as np
import pickle as pkl

class PreprocessPredict(object):
	def __init__(self, image_path, model_path):
		self.image_path = image_path
		self.model = pkl.load(open(model_path, 'rb'))

	def pipeline(self):
		pipe = ImagePipeline(self.image_path)
		pipe.read(sub_dirs=('casual', 'dress'))
		pipe.resize((300, 300, 3))
		pipe.transform(rgb2gray, {})
		pipe.vectorize()
		return pipe

	def predict(self, pipe):
		predicted =  self.model.predict(pipe.features)
		print "precision for knn:", precision_score(pipe.labels, predicted)
		print "recall for knn:", recall_score(pipe.labels, predicted)
		print "f1 for knn:", f1_score(pipe.labels, predicted, average='weighted')

if __name__ == '__main__':
	pp = PreprocessPredict('/Volumes/MacintoshHD/Users/Chris/Desktop/images/testing/', '/Volumes/MacintoshHD/Users/Chris/Desktop/images/model.pkl')
	img = pp.pipeline()
	pp.predict(img)