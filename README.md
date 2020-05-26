community-pricing-project
--------

**Prerequisites**
- Install **pipenv** - `pip install pipenv` (need only once, takes few minutes)
- ```python3 -m venv venv && source venv/bin/activate && pipenv install```

**Start Cluster**
1. Run ```cluster/build-image.sh``` to build hadoop image (Run if there are updates to image)
2. Run ```cluster/start.sh``` to start the hadoop cluster

**Data Ingestion**
1. Run ```db/start.sh``` to start the postgres database
    1. Optionally, to connect to psql command line: `psql -U postgres --host=localhost  --db=pricing`
2. To perform data dump to postgres and subsequently convert to hdfs run ```db/import.sh```
3. Run ```db/stop.sh``` to stop the postgres database outside the container

**Data Processing**
1. Run ```./run.sh``` to run the spark job to generate the output

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