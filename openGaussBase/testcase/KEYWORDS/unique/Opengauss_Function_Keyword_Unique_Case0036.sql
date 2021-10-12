-- @testpoint: opengauss关键字unique(保留)，给已创建的表创建唯一索引


drop table if exists unique_test;
create table unique_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	c_unique text);

create unique index unique_index on unique_test(c_id);

drop index unique_index;

--清理环境
drop table if exists unique_test;