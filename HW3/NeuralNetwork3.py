import numpy as np
import csv 
import sys

TRAIN_IMAGE=sys.argv[1]
TRAIN_LABEL=sys.argv[2]
TEST_IMAGE=sys.argv[3]

train_images = []
with open(TRAIN_IMAGE, newline='') as csvfile:
    temp = csv.reader(csvfile)
    for row in temp:
    	if row !=[]:
	    	train_images.append(row)
train_images = np.asarray(train_images, dtype=np.float64)
train_images = train_images/255
train_images = [np.reshape(i, (784, 1)) for i in train_images]

train_labels = []
with open(TRAIN_LABEL, newline='') as csvfile:
    temp = csv.reader(csvfile)
    for row in temp:
    	if row !=[]:
	    	train_labels.append(row)
train_labels = np.asarray(train_labels, dtype=np.int64)
vector_train_labels = []
for i in train_labels:
	temp = np.zeros((10, 1))
	temp[i] = 1.0
	vector_train_labels.append(temp)
train_data = list(zip(train_images, vector_train_labels))

test_images = []
with open(TEST_IMAGE, newline='') as csvfile:
    temp = csv.reader(csvfile)
    for row in temp:
    	if row !=[]:
	    	test_images.append(row)
test_images = np.asarray(test_images, dtype=np.float64)
test_images = test_images/255 
test_images = [np.reshape(i, (784, 1)) for i in test_images]

epochs = 15
batch_size = 5
learning_rate = 0.2
neurons = [784, 256, 32, 10]
biases = [np.random.randn(y, 1) for y in neurons[1:]] #random 
weights = [np.random.randn(y, x)/np.sqrt(x) for x, y in zip(neurons[:-1], neurons[1:])] #xavier initialization

batches = [train_data[i:i+batch_size] for i in range(0, len(train_data), batch_size)]
for epoch in range(epochs):
	for batch in batches:
	    batch_bias_adjustment = [np.zeros((y, 1)) for y in neurons[1:]]
	    batch_weight_adjustment = [np.zeros((y, x)) for x, y in zip(neurons[:-1], neurons[1:])]
	    for image, label in batch:
	    	temp_output = image
	    	output_cache = [image] 
	    	combined_input_cache=[]
	    	for i in range(3):
	    		I=np.dot(weights[i], temp_output)+biases[i]
	    		combined_input_cache.append(I)
	    		if i!=2:
	    			temp_output = 1.0/(1.0+np.exp(-I))
	    		else:
		    		temp_output = np.exp(I)/np.sum(np.exp(I), axis=0, keepdims=True)
	    		output_cache.append(temp_output)
	    	cur_bias_adjustment = [np.zeros((y, 1)) for y in neurons[1:]]
	    	cur_weight_adjustment = [np.zeros((y, x)) for x, y in zip(neurons[:-1], neurons[1:])] 
    		for layer in range(1, 4):
	    		if layer == 1:
	    			cross_entropy_loss = output_cache[-layer] - label
	    		else:
	    			sigmoid = 1.0/(1.0+np.exp(-combined_input_cache[-layer]))
	    			derivative = sigmoid*(1-sigmoid)
	    			cross_entropy_loss = np.dot(weights[-layer+1].T, cross_entropy_loss) * derivative
	    		cur_weight_adjustment[-layer] = np.dot(cross_entropy_loss, output_cache[-layer-1].T)
    			cur_bias_adjustment[-layer] = cross_entropy_loss
	    	batch_bias_adjustment = [i+j for i,j in zip(batch_bias_adjustment,cur_bias_adjustment)]
	    	batch_weight_adjustment = [i+j for i,j in zip(batch_weight_adjustment,cur_weight_adjustment)]
	    weights = [old-learning_rate*(adjustment/batch_size) for old,adjustment in zip(weights,batch_weight_adjustment)]
	    biases  = [old-learning_rate*(adjustment/batch_size) for old,adjustment in zip(biases,batch_bias_adjustment)]

with open("test_predictions.csv",'w') as f:
	for image in test_images:
		temp=1
		temp_output = image
		for b,w in zip(biases,weights):
			I=np.dot(w,temp_output)+b
			if temp<3:
				temp_output = 1.0/(1.0+np.exp(-I))
				temp+=1
			else:
				temp_output = np.exp(I)/np.sum(np.exp(I), axis=0, keepdims=True)
		prediction = np.argmax(temp_output)
		f.write(str(prediction))
		f.write("\n")
	f.close()