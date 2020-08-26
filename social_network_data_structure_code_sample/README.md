#### Tweet-Node-Message Mapping


#### Motivation of Analysis

The goal of this project is to match a term part of a terms list to a json-delimited tweets data.
The tweet contains a node_id and with this node_id, it then has to be matched to another file that contains
node_id, to find the matching tweet's node_id to the list of node_id. The final output is the term (original to match) to
the message_id from the tweet. `Term -> Tweet -> Node -> (Term,Message_id from Tweet)` 
&nbsp;

The final output can be found in the text files `term_message_mapping_1.txt` for terms1/node1 and `term_message_mapping_2.txt` 
for terms2/nodes2

&nbsp;
    
> Below is a snapshot of the directory. 

 
    ├── social_network_data_structure_code_sample    # Folder containing all scripts
        ├── data/                          # Folder containing data    
        ├── test/                          # Folder containing test python fuctions
        ├── Dockerfile                     # Dockerfile to run
        ├── runDaily.py                    # Command Line script to run
        ├── matchingFunctions.py           # Matching Function
        ├── TermNodeMatch.py               # Data Processing Functions
        ├── term_message_mapping_1.txt     # Term-Message_id Mapping For term1
        ├── term_message_mapping_2.txt     # Term-Message_id Mapping For term2
        ├── free_response.docx             # Response to Questions
        └── README.md

> Below is the code necessary to run the analysis in python3.6. 
```bash

cd social_network_data_structure_code_sample
pip install -r requirements.txt
#replace name_of_file.
file_to_save_locally="name_of_file"

# term1 and node1 are interchangeable to term2 and node2 (and also add additional 
# term & node data into the data folder)

python runDaily.py dumpData data/tweets data/terms1 data/nodes1 $file_to_save_locally
# $file_to_save_locally contains the term-message_id mapping 
```



&nbsp;
&nbsp;
&nbsp;


#### Major Scripts 

`runDaily.py` -> `This is the main function that will have to run inorder for this analysis to run via command line. The variables that will be passed
into this python script will only change ex. tweet, node, message data. The premise of this script is that this runDaily function
is what will be triggered if one wishes to run this analysis daily (with all the variables changing daily via bash)`\
`TermNodeMatch.py` -> `This is the Data Processing script which reads the necessary files and iterates through the 
data and executes the necessary methods for this analysis`\
`TermNodeMatch.py` ->  `Methods containing the core of this analysis, matching set term -> tweet -> node`\
`test/test_termNodeMatch.py` -> `Unit Testing -- 2 tests`

######To Do List
```$xslt

* Check whether there are similar matches for phrase in tweet; this will require some machine learning and processing for FuzzyMatch or Levenshtein Distance.
* Create DockerFile with Volume/Mount so data generated in the container can be copied into one's local directory.
  I had trouble with the Volume and was not able to retrieve the data that was generated in the container.
* What if there are gigabytes of data; writing this code in a Spark Instance might change the flow of the
  `TermNodeMatch.py` (Data Processing) script.
* Create a Airflow pipline that will run this job as well as an error job if triggered (Design part of the free response
  questions).

```
