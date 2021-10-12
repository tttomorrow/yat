--  @testpoint:openGauss关键字snapshot(非保留)，同时作为表名和列名带引号，并进行dml操作,snapshot列的值最终显示为1000

drop table if exists "snapshot" CASCADE;
create table "snapshot"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"snapshot" varchar(100) default 'snapshot'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "snapshot"(c_id,"snapshot") values(1,'hello');
insert into "snapshot"(c_id,"snapshot") values(2,'china');
update "snapshot" set "snapshot"=1000 where "snapshot"='hello';
delete from "snapshot" where "snapshot"='china';
select "snapshot" from "snapshot" where "snapshot"!='hello' order by "snapshot";

drop table "snapshot";

