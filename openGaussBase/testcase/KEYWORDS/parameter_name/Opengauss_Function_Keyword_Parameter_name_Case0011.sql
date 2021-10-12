--  @testpoint:openGauss关键字parameter_name(非保留)，同时作为表名和列名带引号，并进行dml操作,parameter_name列的值最终显示为1000

drop table if exists "parameter_name";
create table "parameter_name"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"parameter_name" varchar(100) default 'parameter_name'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "parameter_name"(c_id,"parameter_name") values(1,'hello');
insert into "parameter_name"(c_id,"parameter_name") values(2,'china');
update "parameter_name" set "parameter_name"=1000 where "parameter_name"='hello';
delete from "parameter_name" where "parameter_name"='china';
select "parameter_name" from "parameter_name" where "parameter_name"!='hello' order by "parameter_name";

drop table "parameter_name";

