-- @testpoint: 创建普通hash分区表，结合视图

--创建hash分区表
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int,p_name varchar,p_age int)
partition by hash(p_id)
(partition p0,
 partition p1,
 partition p2,
 partition p3,
 partition p4);

--创建视图
drop view if exists partition_view;
create view partition_view as select * from partition_hash_tab where p_id != 20;

--向分区表中插入数据
create or replace procedure insert_partition_hash()
as
insert_str varchar;
begin
    for i in 0..5 loop
        insert_str = 'insert into partition_hash_tab values(10),(20),(30);';
        execute immediate insert_str;
    end loop;
end;
/
call insert_partition_hash();

--查看视图中的数据
select * from partition_view;

--清理环境
drop view partition_view;
drop table partition_hash_tab cascade;
drop procedure if exists insert_partition_hash;