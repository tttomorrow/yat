-- @testpoint: interval分区,创建时声明like子句,源表是普通表,新表是分区表,不指定选项

drop table if exists common_table_001;
drop table if exists partition_table_001;

-- 创建普通表作为分区表like的源表
create table common_table_001( 
col_1 smallint primary key check (col_1 > 0),
col_2 char(30) default 'hey boy',
col_3 int unique,
col_4 date,
col_5 boolean, 
col_6 nchar(30),
col_7 float
)with(fillfactor=70);
create unique index idx_001 on common_table_001(col_4);
comment on column common_table_001.col_6 is 'this is a comment to be verified whether new table will create correctly.';
-- 在修改字段storage之前先记录原类型
select attname, attstorage from pg_catalog.pg_attribute where attname = 'col_2' and attrelid = (select oid from pg_class where relname='common_table_001');
alter table common_table_001 alter col_2 set storage main;

-- like不指定任何选项
create table partition_table_001( 
like common_table_001)
partition by range (col_4)
interval ('1 year') 
(
	partition partition_p1 values less than ('2018-01-01'),
	partition partition_p2 values less than ('2019-01-01'),
	partition partition_p3 values less than ('2020-01-01')
);

-- 查看分区信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_001')
order by relname;
	
-- 验证check，不会被继承
insert into partition_table_001 values (-2,'aaa',1,'2016-02-23',true,'aaa',1.1);
-- 验证default,不会被继承，缺省是不包含缺省表达式的，即新表中所有字段的缺省值都是NULL。
insert into partition_table_001 values (2,default,2,'2017-03-23',false,'bbb',2.2);
-- 验证unique，唯一约束不会被继承
insert into partition_table_001 values (3,'ccc',3,'2018-04-23',true,'ccc',3.3);
insert into partition_table_001 values (4,'ccc',3,'2018-04-23',true,'ccc',3.3);
-- 验证注释，不会被继承
select description from pg_description where objoid=(select oid from pg_class where relname=' partition_table_001');
-- 验证索引，唯一索引不会被继承
insert into partition_table_001 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into partition_table_001 values (6,'fff',6,'2020-06-23',false,'fff',6.6);
-- 验证storage,不会被继承
select attname, attstorage from pg_catalog.pg_attribute where attname = 'col_2' and attrelid = (select oid from pg_class where relname='common_table_001');
select attname, attstorage from pg_catalog.pg_attribute where attname = 'col_2' and attrelid = (select oid from pg_class where relname='partition_table_001');

insert into partition_table_001 values (3,'ccc',3,'2018-04-23',true,'ccc',3.3);
insert into partition_table_001 values (4,'ddd',4,'2019-05-23',false,'ddd',4.4);
insert into partition_table_001 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into partition_table_001 values (6,'fff',6,'2021-07-23',false,'fff',6.6);

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