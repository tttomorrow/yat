-- @testpoint: interval分区,创建时声明like子句,源表分区表，新表普通表
drop table if exists partition_table_001;
drop table if exists partition_table_002;

create table partition_table_001(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date,
col_5 boolean,
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 month')
(
	partition partition_table_001_p1 values less than ('2020-03-01'),
	partition partition_table_001_p2 values less than ('2020-04-01'),
	partition partition_table_001_p3 values less than ('2020-05-01')
);

create table partition_table_002(
like partition_table_001);

-- 查看分区信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_002')
order by relname;

-- 插入数据
insert into partition_table_002 values (1,'aaa',1,'2016-02-23',true,'aaa',1.1);
insert into partition_table_002 values (2,'bbb',2,'2017-03-23',false,'bbb',2.2);
insert into partition_table_002 values (3,'ccc',3,'2018-04-23',true,'ccc',3.3);
insert into partition_table_002 values (4,'ddd',4,'2019-05-23',false,'ddd',4.4);
insert into partition_table_002 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into partition_table_002 values (6,'fff',6,'2021-07-23',false,'fff',6.6);

-- 查看分区信息无
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_002')
order by relname;
drop table partition_table_002;
drop table if exists partition_table_001;