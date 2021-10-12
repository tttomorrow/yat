--  @testpoint:openGauss关键字Location(非保留)，同时作为表名和列名带引号，并进行dml操作,Location列的值最终显示为1000

drop table if exists "Location";
create table "Location"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Location" varchar(100) default 'Location'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Location"(c_id,"Location") values(1,'hello');
insert into "Location"(c_id,"Location") values(2,'china');
update "Location" set "Location"=1000 where "Location"='hello';
delete from "Location" where "Location"='china';
select "Location" from "Location" where "Location"!='hello' order by "Location";

drop table "Location";

