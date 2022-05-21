-- @testpoint: List分区表结合LIKE INCLUDING PARTITION参数合理报错

--step1:创建list分区表;expect:成功
drop table if exists t_partition_list_0016_01;
create table t_partition_list_0016_01
(id                         NUMBER(7) CONSTRAINT t_partition_list_0016_01_id_nn NOT NULL,
 use_filename               VARCHAR2(20),
 filename                   VARCHAR2(255),
 text                       VARCHAR2(2000))
partition by list(id)
(partition p1 values(10),
 partition p2 values(20));

--step2:插入数据;expect:成功
insert into t_partition_list_0016_01 values(10,'张三','数学','老师');
insert into t_partition_list_0016_01 values(20,'张三','数学','老师');

--step3:复制表结合LIKE INCLUDING  PARTITION参数;expect:合理报错
drop table if exists t_partition_list_0016_02;
create table t_partition_list_0016_02 (like  t_partition_list_0056_01 INCLUDING PARTITION);

--step4:清理环境;expect:成功
drop table t_partition_list_0016_01;


