--  @testpoint:openGauss关键字Inherit(非保留)，同时作为表名和列名带引号，并进行dml操作,Inherit列的值最终显示为1000

drop table if exists "Inherit";
create table "Inherit"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Inherit" varchar(100) default 'Inherit'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Inherit"(c_id,"Inherit") values(1,'hello');
insert into "Inherit"(c_id,"Inherit") values(2,'china');
update "Inherit" set "Inherit"=1000 where "Inherit"='hello';
delete from "Inherit" where "Inherit"='china';
select "Inherit" from "Inherit" where "Inherit"!='hello' order by "Inherit";

drop table "Inherit";

