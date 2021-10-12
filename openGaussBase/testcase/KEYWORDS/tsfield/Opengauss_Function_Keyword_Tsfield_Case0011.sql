--  @testpoint:openGauss关键字tsfield(非保留)，同时作为表名和列名带引号，并进行dml操作,tsfield列的值最终显示为1000

drop table if exists "tsfield" CASCADE;
create table "tsfield"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"tsfield" varchar(100) default 'tsfield'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "tsfield"(c_id,"tsfield") values(1,'hello');
insert into "tsfield"(c_id,"tsfield") values(2,'china');
update "tsfield" set "tsfield"=1000 where "tsfield"='hello';
delete from "tsfield" where "tsfield"='china';
select "tsfield" from "tsfield" where "tsfield"!='hello' order by "tsfield";

drop table "tsfield";
