--  @testpoint:openGauss关键字Date(非保留)，同时作为表名和列名带引号，并进行dml操作,Date列的值最终显示为1000

drop table if exists "Date";
create table "Date"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Date" varchar(100) default 'Date'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "Date"(c_id,"Date") values(1,'hello');
insert into "Date"(c_id,"Date") values(2,'china');
update "Date" set "Date"=1000 where "Date"='hello';
delete from "Date" where "Date"='china';
select "Date" from "Date" where "Date"!='hello' order by "Date";

drop table "Date";

