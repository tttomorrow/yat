-- @testpoint: List分区表结合LIKE INCLUDING DEFAULTS参数

--step01:创建list分区表;expect:成功
drop table if exists t_partition_list_0052_01;
drop table if exists t_partition_list_0052_02;
create table t_partition_list_0052_01
(id                        number(7),
 use_filename               varchar2(20) ,
 filename                   varchar2(255) default 'test01',
 text                       varchar2(2000))
partition by  list(id)
(partition p1 values(1),
 partition p2 values(2));

--step02:插入数据;expect:成功
insert into t_partition_list_0052_01(id,use_filename,text ) values(1,'张三','老师');
insert into t_partition_list_0052_01(id,use_filename,text ) values(2,'张三','老师');

--step03:查看数据;expect:成功
select * from t_partition_list_0052_01 order by id asc;

--step04:使用like参数建表;expect:成功
create table t_partition_list_0052_02 (like  t_partition_list_0052_01 including defaults);

--step05:插入数据;expect:成功
insert into t_partition_list_0052_02(id,use_filename,text ) values(3,'李四','学生');
insert into t_partition_list_0052_02(id,use_filename,text ) values(4,'李四','学生');

--step06:查看数据;expect:成功
select * from t_partition_list_0052_02 order by id asc;

--step07:清理环境;expect:成功
drop table if exists t_partition_list_0052_01;
drop table if exists t_partition_list_0052_02;
