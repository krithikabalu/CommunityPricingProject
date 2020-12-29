FROM ubuntu:18.04

WORKDIR /root

# install openssh-server, openjdk and wget
RUN apt-get update && apt-get install -y openssh-server openjdk-8-jdk wget vim

# install hadoop
RUN wget https://mirrors.estointernet.in/apache/hadoop/common/hadoop-2.10.1/hadoop-2.10.1.tar.gz&& \
    tar -xzvf hadoop-2.10.1.tar.gz && \
    mv hadoop-2.10.1 /usr/local/hadoop && \
    rm hadoop-2.10.1.tar.gz

# install spark
RUN wget https://archive.apache.org/dist/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz && \
    tar -xvf spark-2.4.5-bin-hadoop2.7.tgz && \
    mv spark-2.4.5-bin-hadoop2.7 /usr/local/spark && \
    rm spark-2.4.5-bin-hadoop2.7.tgz

# install sqoop 1.4.7
RUN wget http://apachemirror.wuchna.com/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz && \
    tar -xvf sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz && \
    mv sqoop-1.4.7.bin__hadoop-2.6.0 /usr/lib/sqoop && \
    rm sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz

# install postgres 42.2.7
RUN wget https://jdbc.postgresql.org/download/postgresql-42.2.7.jre7.jar && \
    mv postgresql-42.2.7.jre7.jar /usr/lib/sqoop/lib

# install hive
RUN wget https://archive.apache.org/dist/hive/hive-2.3.6/apache-hive-2.3.6-bin.tar.gz && tar -xvf apache-hive-2.3.6-bin.tar.gz
RUN wget http://archive.apache.org/dist/db/derby/db-derby-10.12.1.1/db-derby-10.12.1.1-bin.tar.gz && tar -xvf db-derby-10.12.1.1-bin.tar.gz

# install elasticsearch-hadoop
RUN wget https://repo1.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/7.0.0/elasticsearch-hadoop-7.0.0.jar

# install python and other deps
RUN apt install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt update && apt install -y python && apt install -y python-pip
RUN apt-get install -y libgfortran3
RUN pip install numpy
# set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 
ENV HADOOP_HOME=/usr/local/hadoop 
ENV SPARK_HOME=/usr/local/spark
ENV SQOOP_HOME /usr/lib/sqoop
ENV HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
ENV LD_LIBRARY_PATH=/usr/local/hadoop/lib/native:$LD_LIBRARY_PATH
ENV PATH=$PATH:/usr/local/hadoop/bin:/usr/local/hadoop/sbin:/usr/local/spark/bin:$SQOOP_HOME/bin

# ssh without key
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P '' && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

RUN mkdir -p ~/hdfs/namenode && \
    mkdir -p ~/hdfs/datanode && \
    mkdir $HADOOP_HOME/logs

COPY cluster/config/* /tmp/

RUN mv /tmp/ssh_config ~/.ssh/config && \
    mv /tmp/hadoop-env.sh /usr/local/hadoop/etc/hadoop/hadoop-env.sh && \
    mv /tmp/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml && \
    mv /tmp/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml && \
    mv /tmp/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml && \
    mv /tmp/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml && \
    mv /tmp/slaves $HADOOP_HOME/etc/hadoop/slaves && \
    mv /tmp/start-hadoop.sh ~/start-hadoop.sh && \
    mv /tmp/spark-defaults.conf $SPARK_HOME/conf/spark-defaults.conf

# add required files for elasticsearch using hive
RUN mv apache-hive-2.3.6-bin /usr/local/hive && \
    mv db-derby-10.12.1.1-bin /usr/local/derby && \
    mv elasticsearch-hadoop-7.0.0.jar /usr/local/hive/lib && \
    cp /usr/local/hive/conf/hive-env.sh.template /usr/local/hive/conf/hive-env.sh && \
    mv /tmp/hive-site.xml /usr/local/hive/conf/hive-site.xml && \
    rm apache-hive-2.3.6-bin.tar.gz && \
    rm db-derby-10.12.1.1-bin.tar.gz

# set ennvironment variables for hive
ENV HIVE_HOME /usr/local/hive
ENV DERBY_HOME /usr/local/derby
ENV PATH $PATH:$SQOOP_HOME/bin:$HIVE_HOME/bin:$DERBY_HOME/bin
ENV CLASSPATH $CLASSPATH:/usr/local/Hadoop/lib/*:.
ENV CLASSPATH $CLASSPATH:/usr/local/hive/lib/*:.

RUN chmod +x ~/start-hadoop.sh && \
    chmod +x $HADOOP_HOME/sbin/start-dfs.sh && \
    chmod +x $HADOOP_HOME/sbin/start-yarn.sh

# format namenode
RUN /usr/local/hadoop/bin/hdfs namenode -format

CMD [ "sh", "-c", "service ssh start; bash"]


