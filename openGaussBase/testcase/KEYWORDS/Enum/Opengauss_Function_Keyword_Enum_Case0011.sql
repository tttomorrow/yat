--  @testpoint:openGauss关键字enum(非保留)，同时作为表名和列名带引号，并进行dml操作,enum列的值最终显示为1000

drop table if exists "enum";
create table "enum"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"enum" varchar(100) default 'enum'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "enum"(c_id,"enum") values(1,'hello');
insert into "enum"(c_id,"enum") values(2,'china');
update "enum" set "enum"=1000 where "enum"='hello';
delete from "enum" where "enum"='china';
select "enum" from "enum" where "enum"!='hello' order by "enum";

drop table "enum";

