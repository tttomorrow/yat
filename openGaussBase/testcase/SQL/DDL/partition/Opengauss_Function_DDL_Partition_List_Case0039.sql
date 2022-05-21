-- @testpoint: list分区表上以insert方式创建触发器

--step1：创建list分区表,expect成功
drop table if exists t_partition_list_0039_01;
create table t_partition_list_0039_01(p_id int)
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30),
 partition p4 values(40));

--step2：创建普通表,expect成功
drop table if exists t_partition_list_0039_02;
create table t_partition_list_0039_02(p_id int);

--step3：创建触发器函数,expect成功
create or replace function insert_func() returns trigger as
           $$
           declare
           begin
                   insert into t_partition_list_0039_02 values(1);
                   return new;
           end
           $$ language plpgsql;
/

--step4：创建insert触发器,expect成功
create trigger insert_trigger
           before insert on t_partition_list_0039_01
           for each row
           execute procedure insert_func();
/

--step5：在list分区表中插入数据,expect成功
insert into t_partition_list_0039_01 values(10);

--step6：查看触发器是否生效,expect成功
select * from t_partition_list_0039_01;
select * from t_partition_list_0039_02;

--step7：清理环境,expect成功
drop table if exists t_partition_list_0039_01;
drop table if exists t_partition_list_0039_02;
drop function insert_func() ;



