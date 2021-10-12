-- @testpoint: 分区键约束类型 primary key,插入数据重复时合理报错
drop table if exists partition_table_001;

create table partition_table_001( 
COL_1 smallint,
COL_2 char(30),
COL_3 int,
COL_4 TIMESTAMP WITH TIME ZONE primary key,
COL_5 boolean, 
COL_6 nchar(30),
COL_7 float
)
PARTITION BY RANGE (COL_4)
INTERVAL ('1 month') 
(
	PARTITION partition_table_001_p1 VALUES LESS THAN ('2020-03-01 pst'),
	PARTITION partition_table_001_p2 VALUES LESS THAN ('2020-04-01 pst'),
	PARTITION partition_table_001_p3 VALUES LESS THAN ('2020-05-01 pst')
);

insert into partition_table_001 values (1,'aaa',1,'2020-02-23 pst',true,'aaa',1.1);
insert into partition_table_001 values (2,'bbb',2,'2020-03-23 -8',false,'bbb',2.2);
insert into partition_table_001 values (2,'bbb',2,'2020-03-23 -8',false,'bbb',2.2);

drop table if exists partition_table_001;