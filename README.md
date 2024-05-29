# ProductSense_AI
Inspired by OpenAI's GPT, we created ProductSense AI to simplify skin care choices. It offers concise insights on daily skin care products, eliminating the guesswork in ingredient analysis. Our goal? Navigate you smoothly into the realm of conscious consumerism. Join us!


# Environment Setup: 
Make sure pip is installed. In terminal, first install pipenv using command "pip install pipenv". Then run the following command: 
'''bash
pipenv shell  

Open es_NQ_ingestion.ipynb notebook and run all the cells that are not hidden (Hidden cells were used to deploy the elserv2 model which is already deployed in elastic cloud).

Step 1: Elastic search client for pipeline creation.<br>

Step 2: Create index with predefined settings and mappings.<br>

Step 3: Prepare documents to be indexed<br>

Step 4: Ingest to ES<br>

Step 5: Run search to get top k chunks relevant to the query. <br>

k=10 is set and can be modified based on requrements. Additionally, 4 best query strategies are provided.<br>
 Format this properly for Github read me, as I am making changes in github itself. Refine the instruction content so that user can follow better. Include any additional piece of information that might be useful or necessary. 
