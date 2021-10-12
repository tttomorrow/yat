-- @testpoint: 定义mode列不带引号，使用时带双引号或反引号，大小写匹配 合理报错
drop table if exists zsharding_tbl;
create table zsharding_tbl(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	mode char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
insert into zsharding_tbl(c_id,"MODE") values(2,'china');
insert into zsharding_tbl(c_id,`MODE`) values(2,'china');
--清理环境
drop table if exists zsharding_tbl;