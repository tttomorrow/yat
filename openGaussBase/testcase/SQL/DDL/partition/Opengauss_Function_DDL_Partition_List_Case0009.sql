-- @testpoint: 创建普通list分区表，验证分区个数，超过64个 合理报错

--分区个数为0，合理报错
drop table if exists partition_list_tab01;
create table partition_list_tab01(p_id int,p_name varchar,p_age int)
partition by list(p_id);

--分区个数为65,合理报错
drop table if exists partition_list_tab02;
create table partition_list_tab02(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p0 values(0));

create or replace procedure add_partition_list()
as
alter_str varchar;
begin
    for i in 1..64 loop
        alter_str = 'alter table partition_list_tab02 add partition p'||i|| ' values ('||i||');';
		execute immediate alter_str;
    end loop;
end;
/
call add_partition_list();

--清理环境
drop table if exists partition_list_tab02;
drop procedure add_partition_list;
