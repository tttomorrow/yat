--  @testpoint:openGauss关键字password(非保留)，同时作为表名和列名带引号，并进行dml操作,password列的值最终显示为1000

drop table if exists "password";
create table "password"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"password" varchar(100) default 'password'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "password"(c_id,"password") values(1,'hello');
insert into "password"(c_id,"password") values(2,'china');
update "password" set "password"=1000 where "password"='hello';
delete from "password" where "password"='china';
select "password" from "password" where "password"!='hello' order by "password";

drop table "password";

