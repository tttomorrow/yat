-- @testpoint: openGauss关键字nvarchar(非保留)，作为列名带反引号（合理报错）

--step1:建表;expect:失败
drop table if exists t_nvarchar_0003;
create table t_nvarchar_0003(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	`nvarchar` char(50)
)
partition by range (c_integer)
(
	partition p_20180121 values less than (0),
	partition p_20190122 values less than (50000),
	partition p_20200123 values less than (100000),
	partition p_max values less than (maxvalue)
);
