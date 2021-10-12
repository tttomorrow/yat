--  @testpoint:openGauss关键字login(非保留)，同时作为表名和列名带引号，并进行dml操作,login列的值最终显示为1000

drop table if exists "login";
create table "login"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"login" varchar(100) default 'login'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "login"(c_id,"login") values(1,'hello');
insert into "login"(c_id,"login") values(2,'china');
update "login" set "login"=1000 where "login"='hello';
delete from "login" where "login"='china';
select "login" from "login" where "login"!='hello' order by "login";

drop table "login";

