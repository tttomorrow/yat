-- @testpoint: 创建普通list分区表，结合视图

--创建list分区表
drop table if exists partition_list_tab;
create table partition_list_tab(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p0 values(0),
 partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30),
 partition p4 values(40));

--创建视图
drop view if exists partition_view;
create view partition_view as select * from partition_list_tab where p_id != 20;

--向分区表中插入数据
create or replace procedure insert_partition_list()
as
insert_str varchar;
begin
    for i in 0..5 loop
        insert_str = 'insert into partition_list_tab values(10),(20),(30);';
        execute immediate insert_str;
    end loop;
end;
/
call insert_partition_list();

--查看视图中的数据
select * from partition_view order by p_id asc;

--清理环境
drop view partition_view;
drop table partition_list_tab cascade;
drop procedure if exists insert_partition_list;