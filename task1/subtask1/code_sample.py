import json
import random
import argparse
from sklearn.metrics import classification_report

# TODO
# Flags? -train -test etc.

class RandomModel():
    def __init__(self):
        pass
    
    def fit(self,data):
        """
        Learns the seed for future prediction.
        Doesnt use the training file.
        """
        self.seed = random.sample(range(100),1)[0]

    
    def predict(self,test_data):
        """
        Reads the test file and makes predictions based on the seed which was learnt in the fit() part.
        Saves the predictions in the required format.
        """
        
        random.seed(self.seed)
        preds = [{"url":instance['url'],"prediction":random.sample([0,1],1)[0]} for instance in test_data]
        return preds

def read(path):
    """
    Reads the file from the given path (json file).
    Returns list of instance dictionaries.
    """
    data = []
    with open(path,"r") as file:
        for instance in file:
            data.append(json.loads(instance))
    return data

                
def evaluate(goldfile,sysfile,resultfile):
    """
    Takes goldfile (json), sysfile (json) and resultfile (txt).
    Prints out the results on the terminal and saves the same table in the given txt file (resultfile).
    """
    gold = {i["url"]:i["label"] for i in read(goldfile)}
    sys = {i["url"]:i["prediction"] for i in read(sysfile)}
    
    labels, preds = [],[]
    
    for url in gold:
        labels.append(gold[url])
        preds.append(sys[url])
    
    with open(resultfile,'w') as f:
        f.write(classification_report(labels,preds))
        print(classification_report(labels,preds))
        
def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-train_file','--train_file', required=True)
    parser.add_argument('-test_file','--test_file',required=False)
    parser.add_argument('-prediction_output_file','--prediction_output_file',required=False)
    parser.add_argument('-results_output_file','--output_file', required=False)
    args = parser.parse_args()
    return args

def main(train_file,test_file,prediction_output_file,output_file):
    
    #Create model.
    model = RandomModel()
    #Read training data.
    data = read(train_file)
    #Fit. 
    model.fit(data)
    
    #Read test data.
    test_data = read(test_file)
    #Predict and save your results in the required format to the given path (prediction_output_file).
    predictions = model.predict(test_data)
    with open(prediction_output_file,"w") as f:
        for doc in predictions:
            json.dump(doc,f)
            f.write("\n")
                
    #Evaluate sys outputs and save results.
    evaluate(test_file,
             prediction_output_file,
             output_file)
    
if __name__ == "__main__":
    main(*vars(parse()).values())