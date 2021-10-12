--  @testpoint:openGauss关键字sys_refcursor(非保留)，同时作为表名和列名带引号，并进行dml操作,sys_refcursor列的值最终显示为1000

drop table if exists "sys_refcursor" CASCADE;
create table "sys_refcursor"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"sys_refcursor" varchar(100) default 'sys_refcursor'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "sys_refcursor"(c_id,"sys_refcursor") values(1,'hello');
insert into "sys_refcursor"(c_id,"sys_refcursor") values(2,'china');
update "sys_refcursor" set "sys_refcursor"=1000 where "sys_refcursor"='hello';
delete from "sys_refcursor" where "sys_refcursor"='china';
select "sys_refcursor" from "sys_refcursor" where "sys_refcursor"!='hello' order by "sys_refcursor";

drop table "sys_refcursor";

