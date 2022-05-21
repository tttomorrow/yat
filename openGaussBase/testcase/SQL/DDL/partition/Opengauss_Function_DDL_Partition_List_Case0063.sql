-- @testpoint: List分区表与普通表交换数据（对应信息严格一致）（验证表空间）

--step1:创建表空间;expect:成功
create tablespace ts_partition_list_0063 relative location 'tablespace/tablespace_0063';
create tablespace ts_exchange_tablespace relative location 'tablespace/tablespace_0063_02';

--step2:创建list分区表;expect:成功
drop table if exists t_partition_list_0063;
create table t_partition_list_0063(p_id int,p_name varchar,p_age int)
tablespace ts_partition_list_0063
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30));

--step3:插入数据;expect:成功
insert into t_partition_list_0063 values( 10,  '张三', 25);
insert into t_partition_list_0063 values( 10,  '张三', 26);
insert into t_partition_list_0063 values( 20,  '张三', 27);
insert into t_partition_list_0063 values( 20,  '张三', 28);

--step4:创建普通表;expect:成功
drop table if exists exchange_tab;
create table exchange_tab(
p_id int,
p_name varchar,
p_age int)
tablespace ts_exchange_tablespace;

--step5:交换数据;expect:成功
alter table t_partition_list_0063 exchange partition (p1) with table exchange_tab;

--step6:验证表空间信息;expect:成功
select relname from pg_class t1 where relkind='r' and reltablespace=(select oid from pg_tablespace where spcname ='ts_partition_list_0063') order by relname;

--step7:清理环境;expect:成功
drop table if exists t_partition_list_0063;
drop table if exists exchange_tab;
drop tablespace ts_partition_list_0063;
drop tablespace ts_exchange_tablespace;
