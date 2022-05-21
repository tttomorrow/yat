--  @testpoint:openGauss关键字blob(非保留),作为列名带双引号，使用时不带,插入成功
--创建表
drop table if exists blob_test;
create table blob_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer, 
	c_real real, c_double real, 
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38), 
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"blob" char(50)	
) 
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into blob_test(c_id,blob) values(2,'china');

--查询表结构
select * from blob_test;

--清理环境
drop table blob_test;