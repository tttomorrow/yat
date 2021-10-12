-- @testpoint: 创建普通hash分区表，不同分区指定不同表空间

--创建表空间
drop tablespace if exists part_tabspace01;
drop tablespace if exists part_tabspace02;
drop tablespace if exists part_tabspace03;
create tablespace part_tabspace01 relative location 'tablespace/part_tablespace01';
create tablespace part_tabspace02 relative location 'tablespace/part_tablespace02';
create tablespace part_tabspace03 relative location 'tablespace/part_tablespace03';

--创建hash分区表，不同分区指定不同表空间
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int,p_name varchar,p_age int)
partition by hash(p_id)
(partition part_1 tablespace part_tabspace01,
 partition part_2 tablespace part_tabspace02,
 partition part_3 tablespace part_tabspace03);

--循环插入多条数据
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

--查看数据
select count(*) from partition_hash_tab partition (part_1);
select count(*) from partition_hash_tab partition (part_2);
select count(*) from partition_hash_tab partition (part_3);

--查看分区是否在分配的表空间内
select relname, spcname from pg_tablespace t join pg_partition p
on t.oid = p.reltablespace where t.oid in
(select distinct reltablespace from PG_PARTITION where parentid =
(select oid from pg_class where relname='partition_hash_tab')) order by relname desc;

--清理环境
drop table partition_hash_tab;
drop tablespace part_tabspace01;
drop tablespace part_tabspace02;
drop tablespace part_tabspace03;
drop procedure if exists insert_partition_hash;