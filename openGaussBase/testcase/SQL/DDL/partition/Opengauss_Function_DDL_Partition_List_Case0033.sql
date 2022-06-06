-- @testpoint: 创建普通list分区表，结合函数

--step1:创建list分区表,expect成功
drop table if exists t_partition_list_0033;
create table t_partition_list_0033(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30),
 partition p4 values(40));

--step2:创建函数,expect成功
create or replace function insert_partition_list()
return void
as
insert_str varchar;
begin
    for i in 0..5 loop
        insert_str = 'insert into t_partition_list_0033 values(10),(20),(30);';
        execute immediate insert_str;
    end loop;
end;
/

--step3:调用函数，向分区表中插入数据,expect成功
select insert_partition_list();

--step4:查看表中的数据,expect成功
select * from t_partition_list_0033 order by p_id asc;

--step5:清理环境,expect成功
drop table t_partition_list_0033;
drop function insert_partition_list();
