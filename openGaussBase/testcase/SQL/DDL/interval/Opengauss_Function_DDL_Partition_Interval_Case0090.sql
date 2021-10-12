-- @testpoint: interval分区,ALTER TABLE MOVE PARTITION 分区表不存在、分区不存在、表空间不存在时合理报错
drop table if exists mytb9;
drop tablespace if exists tsp9;

create table mytb9(col_4 date not null)
partition by range (col_4)
interval ('1 month')
(partition mytb9_p1 values less than ('2020-02-29'));

create tablespace tsp9 relative location 'partition_table_space/tsp1' maxsize '10m';

-- 分区表不存在
alter table partiton_table_00v move partition sys_p1 tablespace a_tablepace_not_exist;
alter table partiton_table_00v move partition sys_p1 tablespace tsp9;
-- 表分区不存在
alter table mytb9 move partition yoyoyo tablespace tsp9;
alter table mytb9 move partition sys_p1 tablespace tsp9;
-- 表空间不存在
alter table mytb9 move partition sys_p1 tablespace a_tablepace_not_exist;
alter table mytb9 move partition mytb9_p1 tablespace a_tablepace_not_exist;

drop table if exists mytb9;
drop tablespace if exists tsp9;