-- @testpoint: interval分区,创建时声明like子句,源表及新表都是分区表,指定INCLUDING ALL,违背约束合理报错
drop table if exists common_table_001;
drop table if exists partition_table_001;

-- 创建普通表作为分区表like的源表
create table common_table_001(
col_1 smallint check (col_1 > 0),
col_2 char(30) default 'hey boy',
col_3 int,
col_4 date primary key,
col_5 boolean,
col_6 nchar(30),
col_7 float)
partition by range (col_4)
interval ('1 year')
(
	partition partition_p1 values less than ('2018-01-01'),
	partition partition_p2 values less than ('2019-01-01'),
	partition partition_p3 values less than ('2020-01-01')
);
-- 创建唯一索引
create unique index idx_001 on common_table_001(col_4);
-- 创建列注释
comment on column common_table_001.col_6 is 'this is a comment to be verified.';
select description from pg_description where objoid=(select oid from pg_class where relname='common_table_001');
-- 修改字段storage类型
select attname, attstorage from pg_catalog.pg_attribute where attname = 'col_2'
and attrelid = (select oid from pg_class where relname='common_table_001');
alter table common_table_001 alter col_2 set storage main;

-- like指定所有选项
create table partition_table_001(
like common_table_001 including all);

-- 查看分区信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_001')
order by relname;

-- 验证check，被继承
insert into partition_table_001 values (-2,'aaa',1,'2016-02-23',true,'aaa',1.1);
-- 验证default,被继承
insert into partition_table_001 values (2,default,2,'2017-03-23',false,'bbb',2.2);
-- 验证unique，唯一约束被继承
insert into partition_table_001 values (3,'ccc',3,'2018-04-23',true,'ccc',3.3);
insert into partition_table_001 values (4,'ccc',3,'2018-04-23',true,'ccc',3.3);
-- 验证注释，被继承
select description from pg_description where objoid=(select oid from pg_class where relname='partition_table_001');
-- 验证索引，唯一索引被继承
insert into partition_table_001 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into partition_table_001 values (6,'fff',6,'2020-06-23',false,'fff',6.6);
-- 验证storage,被继承
select attname, attstorage from pg_catalog.pg_attribute where attname = 'col_2'
and attrelid = (select oid from pg_class where relname='common_table_001');
select attname, attstorage from pg_catalog.pg_attribute where attname = 'col_2'
and attrelid = (select oid from pg_class where relname='partition_table_001');

-- 查看分区信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_001')
order by relname;

-- 查看各分区中数据
select * from partition_table_001 partition (partition_p1)order by col_4;
select * from partition_table_001 partition (partition_p2)order by col_4;
select * from partition_table_001 partition (partition_p3)order by col_4;
select * from partition_table_001 partition (sys_p1)order by col_4;

drop table if exists common_table_001;
drop table if exists partition_table_001;