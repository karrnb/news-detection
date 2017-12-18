# README #

Readme for NewsDetection on Twitter using Naive Bayes and/or SVM

### What is this repository for? ###

* The code runs on learning datasets to generate a model which can be used to classify tweets into news.
* 1.0

### How do I get set up? ###
* Create two databases "news_classifier" and "news_identifier". Run 'create_tables.sql' in both databases.
* Edit files 'populate_classifier_dataset.py', 'populate_identifier_dataset.py' and 'naive_bayes.py' and add the MySQL credentials of your system.
* Run 'populate_classifier_dataset.py' and 'populate_classifier_dataset.py'
* Run 'naive_bayes.py' twice, with argument 'news_classifier' first and with argument 'news_identifier' second.
* $ naive_bayes.py news_classifier
* $ naive_bayes.py news_identifier
* Run 'predict_custom_input.py' with input argument to test for a given input string.
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests - TBD
* Code review -TBD
* Other guidelines -TBD

### Who do I talk to? ###

* For issues, please contact Repo owner/admin