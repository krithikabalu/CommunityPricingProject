cd db

python setup_data_in_postgres.py

docker exec -it hadoop-master sqoop import -Dmapreduce.job.user.classpath.first=true \
-Dorg.apache.sqoop.splitter.allow_text_splitter=true \
--connect "jdbc:postgresql://postgres:5432/pricing?user=postgres&password=password" --as-avrodatafile \
--target-dir product --table product --split-by product_id