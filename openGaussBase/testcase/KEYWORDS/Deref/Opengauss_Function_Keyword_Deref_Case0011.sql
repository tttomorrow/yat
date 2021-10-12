--  @testpoint:openGauss关键字deref(非保留)，同时作为表名和列名带引号，并进行dml操作,deref列的值最终显示为1000

drop table if exists "deref";
create table "deref"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"deref" varchar(100) default 'deref'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "deref"(c_id,"deref") values(1,'hello');
insert into "deref"(c_id,"deref") values(2,'china');
update "deref" set "deref"=1000 where "deref"='hello';
delete from "deref" where "deref"='china';
select "deref" from "deref" where "deref"!='hello' order by "deref";

drop table "deref";

