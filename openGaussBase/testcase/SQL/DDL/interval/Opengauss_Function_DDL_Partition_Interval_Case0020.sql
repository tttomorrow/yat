-- @testpoint: 分区键包含default
drop table if exists partition_table_001;

create table partition_table_001( 
COL_1 smallint,
COL_2 char(30),
COL_3 int,
COL_4 date default '2020-09-03',
COL_5 boolean, 
COL_6 nchar(30),
COL_7 float
)
PARTITION BY RANGE (COL_4)
INTERVAL ('1 month') 
(
	PARTITION partition_table_001_p1 VALUES LESS THAN ('2020-03-01'),
	PARTITION partition_table_001_p2 VALUES LESS THAN ('2020-04-01'),
	PARTITION partition_table_001_p3 VALUES LESS THAN ('2020-05-01')
);

insert into partition_table_001 values (1,'aaa',1,'2020-02-23',true,'aaa',1.1);
insert into partition_table_001 values (3,'ccc',3,default,true,'ccc',3.3);
insert into partition_table_001 values (4,'ddd',4,'2020-05-23',false,'ddd',4.4);
insert into partition_table_001 values (6,'fff',6,default,false,'fff',6.6);

-- 查看分区信息
select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_001')
order by relname;
	
-- 查看各分区中数据
select * from partition_table_001 partition (partition_table_001_p1)order by COL_4;
select * from partition_table_001 partition (partition_table_001_p2)order by COL_4;
select * from partition_table_001 partition (partition_table_001_p3)order by COL_4;
select * from partition_table_001 partition (sys_p1)order by COL_4;
select * from partition_table_001 partition (sys_p2)order by COL_4;

drop table if exists partition_table_001;
