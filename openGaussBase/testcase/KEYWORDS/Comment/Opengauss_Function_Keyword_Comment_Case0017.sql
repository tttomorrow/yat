-- @testpoint: openGauss关键字comment(非保留)，作为列名不带引号，使用时带单引号或反引号，大小写不匹配(合理报错)
----openGauss关键字comment作为列名不带引号

drop table if exists comment_test;
create table comment_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	comment char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);
insert into comment_test(c_id,'comment') values(2,'china');
insert into comment_test(c_id,`comment`) values(2,'china');
drop table if exists comment_test;
