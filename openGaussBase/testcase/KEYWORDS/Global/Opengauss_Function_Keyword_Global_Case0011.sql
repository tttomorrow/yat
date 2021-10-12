--  @testpoint:openGauss关键字Global(非保留)，同时作为表名和列名带引号，并进行dml操作,Global列的值最终显示为1000

drop table if exists "Global";
create table "Global"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Global" varchar(100) default 'Global'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Global"(c_id,"Global") values(1,'hello');
insert into "Global"(c_id,"Global") values(2,'china');
update "Global" set "Global"=1000 where "Global"='hello';
delete from "Global" where "Global"='china';
select "Global" from "Global" where "Global"!='hello' order by "Global";

drop table "Global";

