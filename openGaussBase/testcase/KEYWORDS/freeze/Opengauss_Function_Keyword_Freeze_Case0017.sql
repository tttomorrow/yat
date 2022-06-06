-- @testpoint: openGauss保留关键字freeze作为列名不带引号，使用时带双引号或反引号，大小写不匹配合理报错
drop table if exists test_tbl;
create table test_tbl(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	freeze char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--插入数据
insert into test_tbl(c_id,"freeze") values(2,'china');
insert into test_tbl(c_id,`freeze`) values(2,'china');

--清理环境
drop table test_tbl;