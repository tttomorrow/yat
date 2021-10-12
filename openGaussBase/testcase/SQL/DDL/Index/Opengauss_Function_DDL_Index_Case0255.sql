-- @testpoint: 验证各种分区表操作对全局分区表索引的破坏能力

-- create table test_ugi_255
drop table if exists test_ugi_255;
create table test_ugi_255
(
    c_id integer not null,
    c_name varchar(16) default 'omm',
    c_class varchar(20) not null
)
partition by range(c_id)
(
    partition p1 values less than (1001), 
    partition p2 values less than (2001), 
    partition p3 values less than (3001),
    partition p4 values less than (4001),
    partition p5 values less than (5001),
    partition p6 values less than (6001)
);

-- insert 6000 rows of data
insert into test_ugi_255(c_id, c_class) select r, '1-1' from generate_series(1,1000) as r;
insert into test_ugi_255(c_id, c_class) select r, '1-2' from generate_series(1001,2000) as r;
insert into test_ugi_255(c_id, c_class) select r, '1-3' from generate_series(2001,3000) as r;
insert into test_ugi_255(c_id, c_class) select r, '1-4' from generate_series(3001,4000) as r;
insert into test_ugi_255(c_id, c_class) select r, '1-5' from generate_series(4001,5000) as r;
insert into test_ugi_255(c_id, c_class) select r, '1-6' from generate_series(5001,6000) as r;
select count(*) from test_ugi_255;

-- create global index
create index global_index_id_041 on test_ugi_255(c_id) global;

-- add partition-can not destroy global_index_id_041
-- global_index_id_041 is usable
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
-- table test_ugi_255 have 6 partitions
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 'test_ugi_255' and t1.parttype = 'p' order by relname;
-- add partition p7
alter table test_ugi_255 add partition p7 values less than (7001);
-- global_index_id_041 is usable
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
-- table test_ugi_255 have 7 partitions now
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 'test_ugi_255' and t1.parttype = 'p' order by relname;

-- drop partition
-- drop partition p7
alter table test_ugi_255 drop partition p7;
-- global_index_id_041 is unusable
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
-- rebuild global_index_id_041
alter index global_index_id_041 rebuild;
-- global_index_id_041 is usable now
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
-- table test_ugi_255 have 6 partitions now
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 'test_ugi_255' and t1.parttype = 'p' order by relname;

-- move partition-can not destroy global_index_id_041
-- create tablespace tableplace_255
drop tablespace if exists tableplace_255;
create tablespace tableplace_255 relative location 'tablespace/tablespace_1';
-- move partition p6 to new tablespace
alter table test_ugi_255 move partition p6 tablespace tableplace_255;
-- global_index_id_041 is usable
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;

-- exchange partition
-- create table test_ugi_255_temp which is use for exchange
drop table if exists test_ugi_255_temp;
create table test_ugi_255_temp
(
    c_id integer not null,
    c_name varchar(16) default 'omm',
    c_class varchar(20) not null
);
insert into test_ugi_255_temp(c_id, c_class) select r, '1-4' from generate_series(3001,3500) as r;
-- inset 500 rows to test_ugi_255_temp
select count(*) from test_ugi_255_temp;
-- exchange partition p4 with table test_ugi_255_temp
alter table test_ugi_255 exchange partition (p4) with table test_ugi_255_temp;
-- global_index_id_041 is unusable now
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
-- table test_ugi_255 contains 5500 rows and table test_ugi_255_temp contains 1000 rows now
select count(*) from test_ugi_255;
select count(*) from test_ugi_255_temp;
-- rebuild global_index_id_041
alter index global_index_id_041 rebuild;
-- global_index_id_041 is usable
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
drop table test_ugi_255_temp;

-- {enable|disable} row movement-can not destroy global_index_id_041
-- enable row movement
alter table test_ugi_255 enable row movement;
-- global_index_id_041 is usable
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;

-- merge partition
-- table test_ugi_255 have 6 partitions
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 'test_ugi_255' and t1.parttype = 'p' order by relname;
-- merge partition p2, p3 into partition p_merge
alter table test_ugi_255 merge partitions p2, p3 into partition p_merge;
-- global_index_id_041 is unusable
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
-- rebuild global_index_id_041
alter index global_index_id_041 rebuild;
-- global_index_id_041 is usable now
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
-- table test_ugi_255 have 5 partitions now
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 'test_ugi_255' and t1.parttype = 'p' order by relname;

-- split partition
-- split partition p_merge into partition p2, p3
alter table test_ugi_255 split partition p_merge at (2001) into (partition p2, partition p3);
-- global_index_id_041 is unusable now
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
-- rebuild global_index_id_041
alter index global_index_id_041 rebuild;
-- global_index_id_041 is usable now
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
-- table test_ugi_255 have 6 partitions
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 'test_ugi_255' and t1.parttype = 'p' order by relname;

-- modify partition-can not destroy global_index_id_041
-- create local index local_index_id_041
create index local_index_id_041 on test_ugi_255(c_id, c_name) local;
-- make local index local_index_id_041 unusable
alter table test_ugi_255 modify partition p4 unusable local indexes;
-- global_index_id_041 is still usable
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
drop index local_index_id_041;

-- truncate partition
-- truncate partition p6
alter table test_ugi_255 truncate partition p6;
-- global_index_id_041 is unusable now
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;
-- rebuild index global_index_id_041
alter index global_index_id_041 rebuild;
-- global_index_id_041 is usable
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid where i.indrelid = 'test_ugi_255'::regclass order by c.relname;

-- clean environment
drop table test_ugi_255;
drop tablespace tableplace_255;