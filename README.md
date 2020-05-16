community-pricing-project
--------

**Prerequisites**
- Install **pipenv** - `pip install pipenv` (need only once, takes few minutes)

**Start Cluster**
1. Run yarn-cluster/build-image.sh to build hadoop image
2. Run yarn-cluster/start.sh to start the hadoop cluster


**Postgres Data**
1. Run postgres/start.sh to start the postgres database
2. To insert data into postgres:
    1. For the first time, to create virtual environment, run: 'python3 -m venv venv'
    2. Activate the venv:  'source venv/bin/activate && pipenv install'
    3. Run 'setup_data_in_postgres.py'
    4. Optionally, to connect to psql command line: `psql -U postgres --host=localhost  --db=pricing`

**Data Ingestion**
1. Use sqoop to import data from postgres to hdfs:
```docker exec -it hadoop-master sqoop import -Dmapreduce.job.user.classpath.first=true -Dorg.apache.sqoop.splitter.allow_text_splitter=true --connect "jdbc:postgresql://postgres:5432/pricing?user=postgres&password=password" --as-avrodatafile --target-dir product --table product --split-by product_id```
2. Run postgres/stop.sh to stop the postgres database outside the container


**Data Visualization**
0. Run ```docker exec -it hadoop-master bash``` if you are outside the container
1. Hive home directory - `cd $HIVE_HOME`
2. Run `hive` and execute the following statements sequentially,

- `CREATE EXTERNAL TABLE product_hdfs (product_id int, description string, cost string, markup string) STORED AS AVRO LOCATION '/user/root/product';`

- `CREATE EXTERNAL TABLE product_es (id bigint, description string, cost float, markup float) STORED BY 'org.elasticsearch.hadoop.hive.EsStorageHandler' TBLPROPERTIES('es.resource' ='pricing/product','es.nodes'= 'elasticsearch');`

- `INSERT OVERWRITE TABLE product_es SELECT * FROM product_hdfs;`

3. Check imported data in elastic search: http://localhost:9200/pricing/_search
4. Finally, create visualisation in Kibana: http://localhost:5601/
    
**Errors/Resolutions**
- ```ERROR tool.ImportTool: Import failed: org.apache.hadoop.mapred.FileAlreadyExistsException: Output directory hdfs://hadoop-master:9000/user/root/product already exists```
    > run **`hadoop fs -rm -r /user/root/product`**