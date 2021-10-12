-- @testpoint: 列名为barrier ，并且定义barrier 列default值
drop table if exists tt;
create  table tt(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_dtte date, c_dttetime date, c_timestamp timestamp,
	barrier text  default 'gauss'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into tt(c_id) values(1);
select * from tt;
drop table if exists tt;