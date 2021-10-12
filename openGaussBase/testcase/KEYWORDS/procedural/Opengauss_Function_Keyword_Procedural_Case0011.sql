--  @testpoint:openGauss关键字procedural(非保留)，同时作为表名和列名带引号，并进行dml操作,procedural列的值最终显示为1000

drop table if exists "procedural";
create table "procedural"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"procedural" varchar(100) default 'procedural'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "procedural"(c_id,"procedural") values(1,'hello');
insert into "procedural"(c_id,"procedural") values(2,'china');
update "procedural" set "procedural"=1000 where "procedural"='hello';
delete from "procedural" where "procedural"='china';
select "procedural" from "procedural" where "procedural"!='hello' order by "procedural";

drop table "procedural";

