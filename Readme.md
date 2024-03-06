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

### Bucketfiles
<ul>
    <li>Choose Space object storage at sidebar</li>
    <li>Create space bucket</li>
    <li>Set name of bucket</li>
    <li>Copy origin endopint then paste in our code to access</li>
    <li>Go to API at sidebar menu</li>
    <li>Copy Secret key & Access key then input in .env code</li>
    <li>Connect it when send the file</li>
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

### Note
Every time the push is successful, the droplet space will be full, it is recommended to delete the droplet cache.
Then also clear the docker cache.
<ul>
    <li>docker ps</li>
    <li>df -h</li>
    <li>docker system prune -a -f --volumes</li>
    <li>Check again df -h</li>
</ul>
