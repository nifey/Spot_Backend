# Spot backend
This is the backend for the spot app. The spot app will identify crops, diseases and suggest treatment for the disease.

The frontend android app for this project can be found [here](https://github.com/AswinChand97/Spot_PHP_test).

It uses the following libraries
* Keras for Machine learning
* Flask for web server

This application was made as a part of Smart India Hackathon 2018 by our team Alpha 6c. The members of the team are 
* Akash
* Abdun Nihaal
* Aswin
* Allwin
* Aravindhan
* Ajith 

The data should be added to the data folder.

To train the model type in 
```python train.py -d data -m models```  

After the models have been created in the models folder ,Run the flask web API interface by typing in
```python app.py```

This is a multilingual application and at present has strings localised in Tamil. The localized string files are present in descriptions folder.
