-- @testpoint: interval分区,创建时声明like子句,源表是普通表,新表是分区表,指定INCLUDING DEFAULTS
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
comment on column common_table_001.col_6 is 'this is a comment to be verified.';
alter table common_table_001 alter col_2 set storage extended;

-- like指定INCLUDING DEFAULTS
create table partition_table_001( 
like common_table_001 including defaults)
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

-- 验证default,继承到了，是'hey boy'
insert into partition_table_001 values (2,default,2,'2017-03-23',false,'bbb',2.2);
select * from partition_table_001;

drop table if exists common_table_001;
drop table if exists partition_table_001;