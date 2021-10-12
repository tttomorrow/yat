--  @testpoint:openGauss关键字minextents(非保留)，同时作为表名和列名带引号，并进行dml操作,minextents列的值最终显示为1000

drop table if exists "minextents";
create table "minextents"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"minextents" varchar(100) default 'minextents'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "minextents"(c_id,"minextents") values(1,'hello');
insert into "minextents"(c_id,"minextents") values(2,'china');
update "minextents" set "minextents"=1000 where "minextents"='hello';
delete from "minextents" where "minextents"='china';
select "minextents" from "minextents" where "minextents"!='hello' order by "minextents";

drop table "minextents";

