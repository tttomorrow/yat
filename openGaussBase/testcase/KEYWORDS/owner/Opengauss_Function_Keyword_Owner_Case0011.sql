--  @testpoint:openGauss关键字owner(非保留)，同时作为表名和列名带引号，并进行dml操作,owner列的值最终显示为1000

drop table if exists "owner";
create table "owner"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"owner" varchar(100) default 'owner'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "owner"(c_id,"owner") values(1,'hello');
insert into "owner"(c_id,"owner") values(2,'china');
update "owner" set "owner"=1000 where "owner"='hello';
delete from "owner" where "owner"='china';
select "owner" from "owner" where "owner"!='hello' order by "owner";

drop table "owner";

