# hotelreviews_sentiment_analysis
Sentiment Analysis on hotel reviews from google travel using BERT transformer.
* We collect dataset via webscrapping with selenium from google travel hotel.
* We explore, clean, and transform the data for it to be used by Pytorch or Tensorflow.
* We build, train, and test a binary sentiment analysis model using BERT architecture with the data.

## Requirements
+ Python version: python 3.8.5. You can create a new conda environment with the command
	```
	conda create -n <yourEnvironmentName> python=3.8.5 anaconda
	```

+ All  packages are in requirements.txt
	* If installing locally, run in terminal
		```bash
		pip install -r requirements.txt
		```
		
	* If using google colab, follow the steps in `BinaryHotelReviews.ipynb` notebook
		1. upload the requirement.txt file in your session. You car run the cell
			```python
			from google.colab import files
			uploaded = files.upload()
			```
		2. Mount google drive and specify an installation path by running the cell containing
			```python
			import os, sys
			from google.colab import drive
			drive.mount('/content/drive')
			nb_path = '/content/notebooks'
			os.symlink('<where in your doogle drive you want to store the env>', nb_path)
			sys.path.insert(0, nb_path)
			```
        3. un-comment the following command and run the cell
			```
			!pip install --target=$nb_path -r requirements.txt
			```
		4. Restart the runtime
		5. Since the requirements are now installed, after closing the session, if you reopen and want to run the notebook again just comment the cell in step 1 and 3, and run only step 2.
		6. Run the cells containing the following command

			```
			!pip install transformers -U 
			```

			```
			!pip install datasets
			```

			```
			!pip install --upgrade pyarrow
			```

## Structure of the project

### Data collection
We used  web scraping with selenium to collect hotel reviews from google travel. The scarping was done using the `ScrapHotelReviews.py` script.

The raw data collected consists of hotel names, reviews and rating.
We got the reviews for hotels in:
* Hanoi
* Macao
* Kuala Lumpur
* Hong Kong
* different cities of Madagascar.

We made sure that the data collected is balanced between positive and negative reviews.

All data are saved in the `data/`  directory.

### Data Eploration Dataset creation
* We explored, cleaned and transform the different collected data.
* Using the data collected from different cities. We created two single ready to use `csv` file, one for multi-class classification and one for binary classification. These two files are saved in the `data/` directory.

### Binary Sentiment Classification
We use BERT transformer with Pytorch to classify positive and negative reviews. We trained only the classification head part of the architecture and froze the lower layers of the BERT model.
