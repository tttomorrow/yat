-- @testpoint: 定义表名和列名为barrier
drop table if exists barrier;
create  table barrier(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_dbarriere date, c_dbarrieretime date, c_timestamp timestamp,
	barrier text  default 'gauss'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);


insert into barrier(c_id,barrier) values(1,'123');
select * from barrier;
drop table if exists barrier;