from skimage import io
from skimage.transform import resize
from pyimage.pipeline import ImagePipeline
from skimage.color import rgb2gray
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pickle as pkl

class PreprocessPredict(object):

	def __init__(self, image_path, model_path):
		self.image_path = image_path
		self.model = pkl.load(open(model_path, 'rb'))


	def read(self):
		return io.imread(self.image_path)

	def do_transforms(self, image):
		img = resize(image, (300, 300, 3))
		return rgb2gray(img)

	def vectorize(self, image):
		return image.flatten()

	def preprocess_vectorize(self):
		img = self.read()
		return self.vectorize(self.do_transforms(img))

	def predict(self, image):
		return self.model.predict(image)

if __name__ == '__main__':
	pp = PreprocessPredict('/Volumes/MacintoshHD/Users/Chris/Desktop/images/test_10.jpg', '/Volumes/MacintoshHD/Users/Chris/Desktop/images/model.pkl')
	img = pp.preprocess_vectorize()
	print pp.predict(img)
