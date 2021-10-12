--  @testpoint:openGauss关键字sysid(非保留)，同时作为表名和列名带引号，并进行dml操作,sysid列的值最终显示为1000

drop table if exists "sysid" CASCADE;
create table "sysid"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"sysid" varchar(100) default 'sysid'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "sysid"(c_id,"sysid") values(1,'hello');
insert into "sysid"(c_id,"sysid") values(2,'china');
update "sysid" set "sysid"=1000 where "sysid"='hello';
delete from "sysid" where "sysid"='china';
select "sysid" from "sysid" where "sysid"!='hello' order by "sysid";

drop table "sysid";

