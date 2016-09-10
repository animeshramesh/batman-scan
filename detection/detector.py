import cv2, nexmo
import scipy.spatial.distance as dist
import sys

# Params = input_file frame_num_For_training

clusters = []	# Global array of cluster objects


def get_HOG_descriptor():
	winSize = (64, 64)
	blockSize = (64, 64)
	blockStride = (32, 32)
	cellSize = (16, 16)
	nbins = 9
	derivAperture = 1
	winSigma = 1.
	histogramNormType = 0
	L2HysThreshold = 2.0000000000000001e-01
	gammaCorrection = 0
	nlevels = 64
	return cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, derivAperture, winSigma,
							histogramNormType, L2HysThreshold, gammaCorrection, nlevels)
                      
class Cluster:
	def __init__(self, centre):
		self.centre = centre
		self.memberCount = 1
		self.radius = 0

def assignCluster(feature, isTrainingPhase):
	global clusters
	if clusters:
		closestCluster = 0
		closestDistance = float("inf")
		for j, cluster in enumerate(clusters):
			x = dist.cosine(feature, cluster.centre) # Determining the cosine distance between vector and cluster center
			if x < closestDistance:
				closestCluster = j
				closestDistance = x

		if clusters[closestCluster].memberCount > 2:
			if closestDistance <=clusters[closestCluster].radius:
				clusters[closestCluster].memberCount+=1
			elif closestDistance < clusters[closestCluster].radius*1.1:
				clusters[closestCluster].memberCount+=1
				clusters[closestCluster].radius = closestDistance
			else:
				if isTrainingPhase:
					clusters.append(Cluster(feature)) # Create a new cluster center
				else:
					return -1
		else:
			clusters[closestCluster].memberCount+=1
			clusters[closestCluster].radius = closestDistance

		return closestDistance

	else:	# Insert first cluster center
		clusters.append(Cluster(feature))
		return 0


def analyze_video(input_file, training_frame_count):

	cap = cv2.VideoCapture(input_file)
	# out = cv2.VideoWriter('vid2_result.avi', cv2.cv.CV_FOURCC(*'XVID'), 30.0, (320,240))

	frame_num=0
	consecutive_anomaly_count = 0
	hog = get_HOG_descriptor()

	while (cap.isOpened()):
		ret, frame = cap.read()
		if frame is None:
			break
		frame_num += 1
		# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)	
		frame = cv2.GaussianBlur(frame,(5,5),0)	# Smooth image by guassian blur
		h = hog.compute(frame)

		distance = assignCluster(h, frame_num <= training_frame_count)	# 2nd param is True for training phase
		# print frame_num, len(clusters), distance 
		if distance == -1: # Frame is detected as anomaly
			consecutive_anomaly_count += 1
			overlay = frame.copy()
			alpha = 0.5
			cv2.rectangle(overlay, (0, 0), (999, 999),(0, 0, 255), -1)
			cv2.addWeighted(overlay,alpha, frame, 1 - alpha, 0, frame)
			if consecutive_anomaly_count > 5:
				nexmo.call_phone("14129831712", "Suspicious activity detected at Wells Fargo Center, Philadelphia")

		else: 
			consecutive_anomaly_count = 0

		cv2.imshow('frame', frame)
		# out.write(frame)
		k = cv2.waitKey(1) & 0xff
		if k == 27:
			break

	cv2.destroyAllWindows()
	cap.release()
	# out.release()

if __name__ == "__main__":
	analyze_video(sys.argv[1], int(sys.argv[2]))

