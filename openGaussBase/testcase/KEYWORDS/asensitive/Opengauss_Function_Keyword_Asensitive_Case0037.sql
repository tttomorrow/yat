-- @testpoint: 列名和表名出现关键字asensitive
drop table if exists asensitive;
create table asensitive(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	asensitive text  default 'gauss'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into asensitive(c_id,asensitive) values(1,'123');
insert into asensitive(c_id) values(2);
select * from asensitive order by 1;
drop table if exists asensitive;