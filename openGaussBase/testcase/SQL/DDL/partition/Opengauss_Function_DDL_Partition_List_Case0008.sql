-- @testpoint: 创建普通list分区表，验证分区个数，在合理范围内

--分区个数小于64
drop table if exists partition_list_tab01;
create table partition_list_tab01(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(10,20,30),
 partition part_2 values(40,50,60),
 partition part_3 values(70,80,90));

--分区个数等于64
drop table if exists partition_list_tab02;
create table partition_list_tab02(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p0 values(0));

create or replace procedure add_partition_list()
as
alter_str varchar;
begin
    for i in 1..63 loop
        alter_str = 'alter table partition_list_tab02 add partition p'||i|| ' values ('||i||');';
		execute immediate alter_str;
    end loop;
end;
/
call add_partition_list();

--查看分区个数是否等于64
select  count(boundaries) from pg_partition
where parentid = (select parentid from pg_partition where relname = 'partition_list_tab02');

--清理环境
drop table if exists partition_list_tab01;
drop table if exists partition_list_tab02;
drop procedure add_partition_list;
