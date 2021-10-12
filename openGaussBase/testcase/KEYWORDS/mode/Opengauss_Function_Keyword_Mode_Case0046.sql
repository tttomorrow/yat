-- @testpoint: 表名和列名同时出现关键字mode，与dml结合
drop table if exists mode;
create table mode(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	mode varchar(100) default 'mode'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);
insert into mode(c_id,mode) values(1,'shijie');
insert into mode(c_id,mode) values(2,'china');
update mode set mode=1000 where mode='shijie';
delete from mode where mode='china';
select mode from mode where mode!='shijie' order by mode;
--清理环境
drop table if exists mode;
