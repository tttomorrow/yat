--  @testpoint:openGauss关键字constructor(非保留)，同时作为表名和列名带引号，并进行dml操作,constructor列的值最终显示为1000

drop table if exists "constructor";
create table "constructor"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"constructor" varchar(100) default 'constructor'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "constructor"(c_id,"constructor") values(1,'hello');
insert into "constructor"(c_id,"constructor") values(2,'china');
update "constructor" set "constructor"=1000 where "constructor"='hello';
delete from "constructor" where "constructor"='china';
select "constructor" from "constructor" where "constructor"!='hello' order by "constructor";

drop table "constructor";

