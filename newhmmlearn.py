import sys 
import math
class hmm_learn():
    
    def __init__(self,nameOfFile):
        self.nameOfFile = nameOfFile
        self.writeInFile = ""
        
    
    def read_file(self):
        with open(self.nameOfFile) as fn:
            hmmLearnData = fn.readlines()
        return hmmLearnData
    
    def write_file(self,output):
        with open("./hmmmodel.txt", "w") as fp:
            fp.write(output)
    
    def calculateTransitionProbability(self,hmmLearnData):
        transition_probability_dict = {}
        for sentence in hmmLearnData:
            wordAndTag = sentence.split()
            #create the previousToken pointer to keep a track of previous token
            #Since in transition probability we will look for the last token only
            previousToken = "<start>"
            endToken = "<end>"
            
            for element in wordAndTag:
                
                #the separator is always the last slash in the word/tag sequence
                word, tag = element.rsplit("/", 1)
                
                
                # token not in dictioary then create a new one
                # e.g.  transition_probability_dict['Noun'] = {}
                if previousToken not in transition_probability_dict:
                    transition_probability_dict[previousToken] = {}
                
                #if the combination of previous tag and current tag not in dictionary
                #then create a one else increment the number of occurance
                #e.g. transition_probability_dict['<start>']['Noun'] = 1
                
                if tag not in transition_probability_dict[previousToken]:
                    transition_probability_dict[previousToken][tag] = 1
                else:
                    transition_probability_dict[previousToken][tag] = transition_probability_dict[previousToken][tag]+1
                
                #Update the previous pointer to the current pointer
                previousToken = tag
                
            #Check for this Portion
            if previousToken not in transition_probability_dict:
                transition_probability_dict[previousToken] = {}
                
            if endToken not in transition_probability_dict[previousToken]:
                transition_probability_dict[previousToken][endToken] = 1
            else:
                 transition_probability_dict[previousToken][endToken] =transition_probability_dict[previousToken][endToken]+ 1
        
        #Perform Smoothing for the transition probability
        transition_probability_dict = self.smoothingTransitionProbability(transition_probability_dict)
        
        return transition_probability_dict

    # Increment all the number by 1, so that if there are any 0 it will become as 1
    def smoothingTransitionProbability(self,transition_probability_dict):
        
        list_of_tags = list(transition_probability_dict.keys())
        list_of_tags += ["<end>"]
        for tag in transition_probability_dict: 
            totalNumberOfTag = 0
            for n_tag in list_of_tags:
                if n_tag not in transition_probability_dict[tag]:
                    transition_probability_dict[tag][n_tag] = 1
                else:
                    transition_probability_dict[tag][n_tag] = transition_probability_dict[tag][n_tag]+1
                    
                totalNumberOfTag=totalNumberOfTag+ transition_probability_dict[tag][n_tag]

            for n_tag in transition_probability_dict[tag]:
                transition_probability_dict[tag][n_tag] = math.log(transition_probability_dict[tag][n_tag]/totalNumberOfTag)
                
        return transition_probability_dict

              
    def calculateEmissionProbability(self,hmmLearnData):
        emission_probability_dict = {}
        for sentence in hmmLearnData:
            # Word/tag
            wordAndTag = sentence.split() #Word/Tag
            for element in wordAndTag:
                
                word, tag = element.rsplit("/", 1) #Word/Tag
                #First Check Whether Tag(eg:Noun) is present in dictionary
                if tag not in emission_probability_dict:
                    emission_probability_dict[tag] = {}
                    
                #If Word is present then simply add 1 to the Count else 
                #Create a dictionary of that word and initialize it to 1
                
                if word in emission_probability_dict[tag]:
                    emission_probability_dict[tag][word] =emission_probability_dict[tag][word]+ 1
                else:
                    emission_probability_dict[tag][word] = 1 
            
                     
                
        for tag in emission_probability_dict:
            
            totalNumberOfTag = 0
            
            #Count the total number of occurance of a tag 
            for word in emission_probability_dict[tag]:
                totalNumberOfTag += emission_probability_dict[tag][word]
            
            #Divide a single Tag Corresponding to a word with the total number of that Tag
            for word in emission_probability_dict[tag]:
                emission_probability_dict[tag][word] = math.log(emission_probability_dict[tag][word]/totalNumberOfTag)
        
        
        
       
        
        
        return emission_probability_dict
    
    
    def main(self):
        hmmLearnData = self.read_file()
        transition_probability_dict = self.calculateTransitionProbability(hmmLearnData)
        emission_probability_dict = self.calculateEmissionProbability(hmmLearnData)

        for tag in emission_probability_dict:
            self.writeInFile += "[{} {}]".format("Emission",tag)
            for word in emission_probability_dict[tag]:
                self.writeInFile += " {}||{}".format(word,emission_probability_dict[tag][word])
            self.writeInFile += "\n"
        
        for tag in transition_probability_dict:
            self.writeInFile += "[{} {}]".format("Transition",tag)
            for allTag in transition_probability_dict[tag]:
                self.writeInFile += " {}||{} ".format(allTag,transition_probability_dict[tag][allTag])
            self.writeInFile += "\n"
      
        self.writeInFile = self.writeInFile[:-1]
        self.write_file(self.writeInFile)



hmmLearnFile = sys.argv[1]
obj = hmm_learn(hmmLearnFile)
obj.main()