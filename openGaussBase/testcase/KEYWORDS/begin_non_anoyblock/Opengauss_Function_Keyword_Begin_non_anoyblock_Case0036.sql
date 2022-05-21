-- @testpoint: 定义表名和列名为begin_non_anoyblock
drop table if exists begin_non_anoyblock;
create  table begin_non_anoyblock(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_dbegin_non_anoyblocke date, c_dbegin_non_anoyblocketime date, c_timestamp timestamp,
	begin_non_anoyblock text  default 'gauss'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);


insert into begin_non_anoyblock(c_id,begin_non_anoyblock) values(1,'123');
select * from begin_non_anoyblock;
drop table if exists begin_non_anoyblock;