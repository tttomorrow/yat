--  @testpoint:openGauss关键字deferred(非保留)，同时作为表名和列名带引号，并进行dml操作,deferred列的值最终显示为1000

drop table if exists "deferred";
create table "deferred"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"deferred" varchar(100) default 'deferred'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "deferred"(c_id,"deferred") values(1,'hello');
insert into "deferred"(c_id,"deferred") values(2,'china');
update "deferred" set "deferred"=1000 where "deferred"='hello';
delete from "deferred" where "deferred"='china';
select "deferred" from "deferred" where "deferred"!='hello' order by "deferred";

drop table "deferred";

