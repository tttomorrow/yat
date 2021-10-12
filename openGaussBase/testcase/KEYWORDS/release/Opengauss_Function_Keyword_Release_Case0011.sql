--  @testpoint:openGauss关键字release(非保留)，同时作为表名和列名带引号，并进行dml操作,release列的值最终显示为1000

drop table if exists "release";
create table "release"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"release" varchar(100) default 'release'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "release"(c_id,"release") values(1,'hello');
insert into "release"(c_id,"release") values(2,'china');
update "release" set "release"=1000 where "release"='hello';
delete from "release" where "release"='china';
select "release" from "release" where "release"!='hello' order by "release";

drop table "release";

