-- @testpoint: 创建hash行存表并进行增删改查等操作

drop table if exists partition_table_004;
create table partition_table_004
(
c_smallint smallint not null,
c_integer integer,
c_bigint bigint,
c_decimal decimal,
c_numeric numeric,
c_real real,
c_double  double precision,
c_character_1 character varying(100)  not null,
c_varchar varchar(100),
c_character_2 character(100),
c_char_1 char(8000),
c_character_3 character(100),
c_char_2 char(8000),
c_text text,
c_nvarchar2 nvarchar2(2000),
c_timestamp_1 timestamp without time zone  ,
c_timestamp_2 timestamp with time zone ,
c_date date
)partition by range (c_timestamp_1)
(
partition hash_partition_table_004_01  values less than ('1954-2-6 13:12:12.2356'),
partition hash_partition_table_004_02  values less than ('1964-2-6 13:12:12.2356'),
partition hash_partition_table_004_03  values less than ('2064-2-6 13:12:12.2356')
);
--I2.插入数据
--S1.向表中插入数据
insert into partition_table_004
 (c_smallint,c_integer,c_bigint,c_decimal,c_numeric,c_real,c_character_1,c_varchar,c_character_2,c_char_1,c_character_3,c_char_2,c_text,c_nvarchar2,c_timestamp_1,c_timestamp_2,c_date)
 values (7,-20,150,40.3,4.3,6.2,160.25,'155','h','DEF','A','A','HK','aaaa','1949-02-06 13:12:12.2356','1949-02-07 13:12:12.2356','1949-02-08 13:12:12'),
(9,-10,100,100.3,10.3,10.2,1000.25,'ABCD','ABC','DEF','A','A','HK','aaaa','1953-02-06 13:12:12.2356','1953-02-07 13:12:12.2356','1953-02-08 13:12:12'),
(19,-10,200,200.3,20.3,20.2,1000.25,'ghgjnh','AgfgfBC','hyh','A','A','HK','aaaa','1952-02-06 13:12:12.2356','1952-02-07 13:12:12.2356','1952-02-08 13:12:12');
--I3.更新数据
--S1.更新表数据
update partition_table_004 set c_timestamp_1='1953-01-14 13:12:12.2356', c_timestamp_2='1953-01-15 13:12:12.2356' , c_date='1953-01-16 13:12:12' ;

--I4.查询数据
--S1.查询数据，验证上上步更新操作
select trim(c_timestamp_1),trim(c_timestamp_2),trim(c_date) from partition_table_004;
--I5.删除表数据
--S1.删除表的全部数据
delete from partition_table_004;
--I6.查询数据
--S1.查询数据，验证上步删除数据
select trim(c_timestamp_1),trim(c_timestamp_2),trim(c_date) from partition_table_004;
drop table if exists partition_table_004;