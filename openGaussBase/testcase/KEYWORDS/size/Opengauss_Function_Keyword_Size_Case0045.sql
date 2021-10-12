-- @testpoint: 表名和列名同时出现关键字size，与dml结合
drop table if exists size;
create table size(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	size varchar(100) default 'size'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
insert into size(c_id,size) values(1,'world');
insert into size(c_id,size) values(2,'china');
update size set size=1000 where size='world';
delete from size where size='china';
select size from size where size!='world' order by size;
drop table if exists size;