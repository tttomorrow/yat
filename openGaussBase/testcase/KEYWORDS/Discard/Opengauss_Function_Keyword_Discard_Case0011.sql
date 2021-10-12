--  @testpoint:openGauss关键字discard(非保留)，同时作为表名和列名带引号，并进行dml操作,discard列的值最终显示为1000

drop table if exists "discard";
create table "discard"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"discard" varchar(100) default 'discard'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "discard"(c_id,"discard") values(1,'hello');
insert into "discard"(c_id,"discard") values(2,'china');
update "discard" set "discard"=1000 where "discard"='hello';
delete from "discard" where "discard"='china';
select "discard" from "discard" where "discard"!='hello' order by "discard";

drop table "discard";

