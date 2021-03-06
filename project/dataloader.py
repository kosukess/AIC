import os
import json
import cv2
import numpy as np

class dataloader:
    
    
    def __init__(self, path, label_file, test_label):
        self.train_path = path+"training/"
        self.test_path = path+"testing/"
        self.label_path = path+label_file
        self.test_label_path = path+test_label
        self.train_data = []
        self.train_images  =[]
        self.train_file_name = []
        self.test_data = []
        self.test_images = []
        self.test_file_name = []
        self.labels_train = []
        self.labels_test = []
        self.load_hand_dataset(self.train_path, self.test_path)
        self._assert_exist(self.label_path)
        self._assert_exist(self.test_label_path)
        self.load_labels(self.label_path, self.test_label_path)
        
        self.TOTAL_SAMPLES_PER_CLASS = 100
        
       
        
    def _assert_exist(self, label_path):
        msg = 'File is not availble: %s' % label_path
        assert os.path.exists(label_path), msg
    def load_labels(self, label_path, test_label):
        """
        loads the training and testing labels from a json file
        """
        self._assert_exist(label_path)
        self._assert_exist(test_label)
        with open(label_path, 'r') as f:
            label_data = json.load(f)
        self.labels_train = label_data["labels"]
        with open(test_label, 'r') as f:
            test_label = json.load(f)
        self.labels_test = test_label["labels"]
        
        #return labels_train, labels_test
    def scaled_data(self, train_data, test_data):
        """
        This method helps scaling/normalizing data
        """
        raw_scaler = preprocessing.StandardScaler().fit(train_data)
        scaled_train_data = raw_scaler.transform(train_data)
        scaled_test_data = raw_scaler.transform(test_data)
        return scaled_train_data, scaled_test_data, raw_scaler
    def load_hand_dataset(self, train_path, test_path):
        """
        This method loads the images for training the classifier. 
        """
        WIDTH = 224
        HEIGHT = 224
        for filename in sorted(os.listdir(train_path)):
            print(filename)
            if filename == '.ipynb_checkpoints':
                continue
            self.train_file_name.append(filename)
            image = cv2.imread(train_path+filename)
            #image = image[:, ::-1, :]
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (WIDTH, HEIGHT), interpolation = cv2.INTER_AREA)
            self.train_data.append(np.reshape(np.array(image), 150528))
            self.train_images.append(image)
     
        for filename in sorted(os.listdir(test_path)):
            print(filename)
            if filename == '.ipynb_checkpoints':
                continue
            self.test_file_name.append(filename)
            image = cv2.imread(test_path+filename)
            #image = image[:, ::-1, :]
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (WIDTH, HEIGHT), interpolation = cv2.INTER_AREA)
            self.test_images.append(image)
            self.test_data.append(np.reshape(np.array(image), 150528))
        #return train_images, test_images, train_data, test_data
    def smaller_dataset(self, dataset, no_samples_per_class, no_of_classes):
        """
        This method helps training with a subset of the dataset 
        """
        
        start = 0
        end = no_samples_per_class
        new_dataset = []
        labels = []
        for i in range(no_of_classes):
            new_data = dataset[start:end]
            start = start+self.TOTAL_SAMPLES_PER_CLASS
            end = start+no_samples_per_class
            new_dataset.extend(new_data)
            labels.extend([i+1]*no_samples_per_class)
        return new_dataset, labels           
