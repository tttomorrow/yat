-- @testpoint: 列名为C ，并且定义C列default值
drop table if exists tt;
create  table tt(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_dtte date, c_dttetime date, c_timestamp timestamp,
	C text  default 'gauss'
);


insert into tt (c_id,C) values(1,'123');
insert into tt (c_id) values(2);
select * from tt;
drop table if exists tt;