--  @testpoint:openGauss关键字scope(非保留)，同时作为表名和列名带引号，并进行dml操作,scope列的值最终显示为1000

drop table if exists "scope" CASCADE;
create table "scope"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"scope" varchar(100) default 'scope'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "scope"(c_id,"scope") values(1,'hello');
insert into "scope"(c_id,"scope") values(2,'china');
update "scope" set "scope"=1000 where "scope"='hello';
delete from "scope" where "scope"='china';
select "scope" from "scope" where "scope"!='hello' order by "scope";

drop table "scope";

