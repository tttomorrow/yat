--  @testpoint:openGauss关键字bit_length(非保留)，作为列名不带引号，使用时带单引号或反引号，大小写匹配(合理报错)
----openGauss关键字bit_length作为列名不带引号
--创建表
drop table if exists bit_length_test;
create table bit_length_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	bit_length char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据-合理报错
insert into bit_length_test(c_id,'bit_length') values(2,'china');
insert into bit_length_test(c_id,`bit_length`) values(2,'china');

--清理环境
drop table bit_length_test;
