-- @testpoint: 创建普通list分区表，不同分区指定不同表空间

--创建表空间
drop tablespace if exists part_tabspace01;
drop tablespace if exists part_tabspace02;
drop tablespace if exists part_tabspace03;
create tablespace part_tabspace01 relative location 'tablespace/part_tablespace01';
create tablespace part_tabspace02 relative location 'tablespace/part_tablespace02';
create tablespace part_tabspace03 relative location 'tablespace/part_tablespace03';

--创建list分区表，不同分区指定不同表空间
drop table if exists partition_list_tab;
create table partition_list_tab(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(10) tablespace part_tabspace01,
 partition part_2 values(20) tablespace part_tabspace02,
 partition part_3 values(30) tablespace part_tabspace03);

--循环插入多条数据
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

--查看数据
select count(*) from partition_list_tab partition for ('10');
select count(*) from partition_list_tab partition for ('20');
select count(*) from partition_list_tab partition for ('30');

--查看分区是否在分配的表空间内
select relname, spcname from pg_tablespace t join pg_partition p
on t.oid = p.reltablespace where t.oid in
(select distinct reltablespace from PG_PARTITION where parentid =
(select oid from pg_class where relname='partition_list_tab')) order by relname desc;

--清理环境
drop table partition_list_tab;
drop tablespace part_tabspace01;
drop tablespace part_tabspace02;
drop tablespace part_tabspace03;
drop procedure if exists insert_partition_list;