-- @testpoint: Hash分区表与普通表交换数据（对应信息严格一致）（验证表空间）

--step1：创建表空间 expect：成功
drop tablespace if exists partition_tablespace;
drop tablespace if exists exchange_tablespace;
create tablespace partition_tablespace relative location 'tablespace/tablespace_2';
create tablespace exchange_tablespace relative location 'tablespace/tablespace_3';

--step2：创建hash分区表 expect：成功
drop table if exists t_partition_hash_0078_01;
create table t_partition_hash_0078_01(
id int,
name varchar(100),
age int)
tablespace partition_tablespace
partition by hash(id)
(partition p1,
 partition p2);

--step3：插入数据 expect：成功插入四条数据
insert into t_partition_hash_0078_01 values( 1,  '张三', 25);
insert into t_partition_hash_0078_01 values( 2,  '张三', 26);
insert into t_partition_hash_0078_01 values( 3,  '张三', 27);
insert into t_partition_hash_0078_01 values( 4,  '张三', 28);

--step4：创建普通表 expect：成功
drop table if exists t_partition_hash_0078_02;
create table t_partition_hash_0078_02(
id int,
name varchar(100),
age int)
tablespace exchange_tablespace;

--step5：验证表空间信息 expect：表空间partition_tablespace包含分区表
select relname from pg_class t1 where relkind='r' and reltablespace=(
    select oid from pg_tablespace where spcname ='partition_tablespace');

--step6：验证表空间信息 expect：表空间exchange_tablespace包含普通表
select relname from pg_class t1 where relkind='r' and reltablespace=(
    select oid from pg_tablespace where spcname ='exchange_tablespace');

--step7：交换数据 expect：分区表p1分区与普通表交换信息成功
alter table t_partition_hash_0078_01 exchange partition (p1) with table t_partition_hash_0078_02;

--step8：验证表空间信息 expect：表空间partition_tablespace中包含普通表
select relname from pg_class t1 where relkind='r' and reltablespace=(
    select oid from pg_tablespace where spcname ='partition_tablespace') order by relname asc;

--step9：验证表空间信息 expect：表空间exchange_tablespace不包含普通表
select relname from pg_class t1 where relkind='r' and reltablespace=(
    select oid from pg_tablespace where spcname ='exchange_tablespace');

--step10：清理环境 expect：成功
drop table if exists t_partition_hash_0078_01;
drop table if exists t_partition_hash_0078_02;
drop tablespace partition_tablespace;
drop tablespace exchange_tablespace;