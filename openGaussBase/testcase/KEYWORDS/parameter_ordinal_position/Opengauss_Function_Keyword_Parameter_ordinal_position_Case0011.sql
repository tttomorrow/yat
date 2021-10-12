--  @testpoint:openGauss关键字parameter_ordinal_position(非保留)，同时作为表名和列名带引号，并进行dml操作,parameter_ordinal_position列的值最终显示为1000

drop table if exists "parameter_ordinal_position";
create table "parameter_ordinal_position"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"parameter_ordinal_position" varchar(100) default 'parameter_ordinal_position'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "parameter_ordinal_position"(c_id,"parameter_ordinal_position") values(1,'hello');
insert into "parameter_ordinal_position"(c_id,"parameter_ordinal_position") values(2,'china');
update "parameter_ordinal_position" set "parameter_ordinal_position"=1000 where "parameter_ordinal_position"='hello';
delete from "parameter_ordinal_position" where "parameter_ordinal_position"='china';
select "parameter_ordinal_position" from "parameter_ordinal_position" where "parameter_ordinal_position"!='hello' order by "parameter_ordinal_position";

drop table "parameter_ordinal_position";

