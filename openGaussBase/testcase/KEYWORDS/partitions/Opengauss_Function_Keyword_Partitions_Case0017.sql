--  @testpoint:openGauss关键字partitions(非保留)，作为列名不带引号，使用时带单引号或反引号，大小写匹配(合理报错)
----openGauss关键字partitions作为列名不带引号

drop table if exists partitions_test;
create table partitions_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	partitions char(50)
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
insert into partitions_test(c_id,'partitions') values(2,'china');
insert into partitions_test(c_id,`partitions`) values(2,'china');
drop table partitions_test;
