-- @testpoint: 更新时，使用share列
drop table if exists zsharding_tbl;
create table zsharding_tbl(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	share varchar(100) default 'share'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

insert into zsharding_tbl(c_id,share) values(1,'world');
insert into zsharding_tbl(c_id) values(2);
update zsharding_tbl set share=100;
select * from zsharding_tbl order by share;
drop table if exists zsharding_tbl;