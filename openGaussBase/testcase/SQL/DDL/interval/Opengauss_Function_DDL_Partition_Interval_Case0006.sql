-- @testpoint: interval分区,分区键数据类型为timestamp without time zone/timestamp
drop table if exists partition_table_001;

create table partition_table_001 (logdate timestamp without time zone not null) 
partition by range (logdate)
interval ('1 month') 
(
	partition partition_table_001_p1 values less than ('2020-03-01'),
	partition partition_table_001_p2 values less than ('2020-04-01'),
	partition partition_table_001_p3 values less than ('2020-05-01')
);

-- 查看分区信息
select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_001')
order by relname;

insert into partition_table_001 values ('2020-02-23');
insert into partition_table_001 values ('2020-03-23');
insert into partition_table_001 values ('2020-04-23');
insert into partition_table_001 values ('2020-05-23');
insert into partition_table_001 values ('2020-06-23');
insert into partition_table_001 values ('2020-07-23');

-- 查看分区信息
select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_001')
order by relname;
	
-- 查看各分区中数据
select * from partition_table_001 partition (partition_table_001_p1)order by logdate;
select * from partition_table_001 partition (partition_table_001_p2)order by logdate;
select * from partition_table_001 partition (partition_table_001_p3)order by logdate;
select * from partition_table_001 partition (sys_p1)order by logdate;
select * from partition_table_001 partition (sys_p2)order by logdate;
select * from partition_table_001 partition (sys_p3)order by logdate;

drop table if exists partition_table_001;

create table partition_table_001 (logdate timestamp not null) 
partition by range (logdate)
interval ('1 month') 
(
	partition partition_table_001_p1 values less than ('2020-03-01'),
	partition partition_table_001_p2 values less than ('2020-04-01'),
	partition partition_table_001_p3 values less than ('2020-05-01')
);

-- 查看分区信息
select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_001')
order by relname;

insert into partition_table_001 values ('2020-02-23');
insert into partition_table_001 values ('2020-03-23');
insert into partition_table_001 values ('2020-04-23');
insert into partition_table_001 values ('2020-05-23');
insert into partition_table_001 values ('2020-06-23');
insert into partition_table_001 values ('2020-07-23');

-- 查看分区信息
select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_001')
order by relname;
	
-- 查看各分区中数据
select * from partition_table_001 partition (partition_table_001_p1)order by logdate;
select * from partition_table_001 partition (partition_table_001_p2)order by logdate;
select * from partition_table_001 partition (partition_table_001_p3)order by logdate;
select * from partition_table_001 partition (sys_p1)order by logdate;
select * from partition_table_001 partition (sys_p2)order by logdate;
select * from partition_table_001 partition (sys_p3)order by logdate;

drop table if exists partition_table_001;
