#### Stock Monthly High/Low


#### Motivation of Analysis

The goal of this assignment is to use AlphaVantage's API to retrieve the maximum high price and 
the minimum low price of every month for any stock. 

Using console, the final output can either be a printed response or can be stored into a text file for further analysis. 

&nbsp;
    
> Below is a snapshot of the directory. 

 
    ├── stock_analysis                             # Folder containing all scripts
        ├── tests/                          # Folder containing tests    
            ├── test_api_output.py          # unit tests
        ├── Dockerfile                      # Dockerfile to run
        ├── api.py                          # api functions
        ├── formatOutput.py                 # format api data
        ├── summarizeOutput.py              # combines methods in api and formatOutput
        ├── runMain.py                      # main function to run
        ├── config.ini                      # Configure File containing API Key
        └── README.md

> Below is the code necessary to run the analysis in python3.6 locally. 
```bash
cd stock_analysis
pip install -r requirements.txt

stock_ticker="replace to desired symbol"

python runMain.py $stock_ticker

# Below if you would like to save output to text file.
python runMain.py > stock_output_${stock_ticker}.txt
 
```


> Below is the code necessary to run the analysis in Docker. 
```bash
cd stock_analysis
docker build .
#find the image_id from code below
docker container ls -la
image_id=""
docker run -it --entrypoint /bin/bash image_id


# in docker terminal
stock_ticker="replace to desired symbol"

python runMain.py $stock_ticker

# Below if you would like to save output to text file.
python runMain.py > stock_output_${stock_ticker}.txt
 
```


&nbsp;



#### Major Scripts 

`api.py` -> `This script contains the api endpoint to retrieve data from AlphaVintage.`\
`formatOutput.py` -> `This script contains the core methods used to format the api result to
output the desired high/low prices for every month of a given stock. `\
`summarizeOutput` -> `This is the method that will be called to retrieve the desired output.`\
`config.ini` ->  `Config. file containing the API key.`\
`test/test_api_output.py` -> `Unit Testing -- 7 tests`

