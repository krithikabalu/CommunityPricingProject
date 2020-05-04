**Steps**
1. Run yarn-cluster/build-image.sh to build hadoop image
2. Run yarn-cluster/start.sh to start the hadoop cluster
3. Run postgres/start.sh to start the postgres database
4. To insert data into postgres:
    1. For the first time, to create virtual environment, run: 'python3 -m venv venv'
    2. Activate the venv:  'source venv/bin/activate && pipenv install'
    3. Run 'setup_data_in_postgres.py'
    4. Optionally, to connect to psql command line: 'psql -U postgres --host=localhost  --db=pricing'
5. Running a sqoop job from hadoop master:
```sqoop import -Dorg.apache.sqoop.splitter.allow_text_splitter=true --connect "jdbc:postgresql://postgres:5432/pricing?user=postgres&password=password" --as-avrodatafile --target-dir product --table product --split-by product_id```
    