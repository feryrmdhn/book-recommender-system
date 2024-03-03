# Books Classification & Recommender System

This is a learning project on a real case study<br/>

There are several models used in this project, including:
<ul>
    <li>Word2Vec</li>
    <li>Naive Bayes</li>
    <li>Naive Bayes with Random Search (Tuning)</li>
    <li>Naive Bayes with Optuna (Tuning)</li>
    <li>ANN</li>
    <li>ANN with Optuna (Tuning)</li>
</ul>

For initial setup, please follow the guide of README here https://github.com/feryrmdhn/mlops-via-ssh<br/>

### Setup Postgre SQL in Digital Ocean
<ul>
    <li>Choose <b>Database</b> at sidebar menu</li>
    <li>Create Database</li>
    <li>Select Engine DB (Postgre) and Plan</li>
    <li>Create new DB</li>
    <li>Select tab overview and <code>choose public network</code> for connection</li>
    <li>Add all secret DB in .env</li>
    <li>Run code store data to DB (in this case <i>db_store.py</i>)</li>
    <li>Run Database extension in VScode</li>
    <li>Insert all secret DB then <code>connect</code></li>
    <li>Check data in DB</li>
</ul>

### Setup Cronjob
To see the setup code, please go to <i>schedule.yml</i>

The next, create dummy data with genre <code>NULL</code> because it will be predicted automatically with cronjob

### Assets
There is a link to see the machine learning code specifications on Google Colab:
<ul>
    <li>https://colab.research.google.com/drive/1cN3YZh7JOjY_8LS5gO_o4bK8s3t3XG4k?usp=sharing</li>
    <li>https://colab.research.google.com/drive/1aTZMaXj76f0mZoFVlliagUPQulpoXzIt?usp=sharing</li>
</ul>
