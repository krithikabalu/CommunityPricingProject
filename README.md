**Steps**
1. Run yarn-cluster/build-image.sh to build hadoop image
2. Run yarn-cluster/start.sh to start the hadoop cluster
3. Run postgres/start.sh to start the postgres database
4. To insert data into postgres:
    1. For the first time, to create virtual environment, run: 'python3 -m venv venv'
    2. Install pipenv - `pip install pipenv` (takes few minutes)
    3. Activate the venv:  'source venv/bin/activate && pipenv install'
    4. Run 'setup_data_in_postgres.py'
    5. Optionally, to connect to psql command line: `psql -U postgres --host=localhost  --db=pricing`
5. Use sqoop to import data from postgres to hdfs:
```sqoop import -Dorg.apache.sqoop.splitter.allow_text_splitter=true --connect "jdbc:postgresql://postgres:5432/pricing?user=postgres&password=password" --as-avrodatafile --target-dir product --table product --split-by product_id```
    - Errors/Resolutions
        - ```Error: org.apache.avro.reflect.ReflectData.addLogicalTypeConversion(Lorg/apache/avro/Conversion;)V```: **add `-Dmapreduce.job.user.classpath.first=true` next to sqoop import if you get**
        - ```ERROR tool.ImportTool: Import failed: org.apache.hadoop.mapred.FileAlreadyExistsException: Output directory hdfs://hadoop-master:9000/user/root/product already exists```: **run `hadoop fs -rm -r /user/root/product`**