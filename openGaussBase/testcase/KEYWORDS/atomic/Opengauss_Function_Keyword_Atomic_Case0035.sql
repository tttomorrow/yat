-- @testpoint: 列名为atomic，并且定义atomic列default值
drop table if exists atomic;
create  table atomic(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_datomice date, c_datomicetime date, c_timestamp timestamp,
	atomic text  default 'gauss'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into atomic(c_id,atomic) values(1,'123');
select * from atomic;
drop table if exists atomic;