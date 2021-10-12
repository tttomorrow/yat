--  @testpoint:openGauss关键字g(非保留)，同时作为表名和列名带引号，并进行dml操作,g列的值最终显示为1000

drop table if exists "g";
create table "g"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"g" varchar(100) default 'g'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "g"(c_id,"g") values(1,'hello');
insert into "g"(c_id,"g") values(2,'china');
update "g" set "g"=1000 where "g"='hello';
delete from "g" where "g"='china';
select "g" from "g" where "g"!='hello' order by "g";

drop table "g";

