--  @testpoint:openGauss关键字data(非保留)，同时作为表名和列名带引号，并进行dml操作,data列的值最终显示为1000

drop table if exists "data";
create table "data"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"data" varchar(100) default 'data'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "data"(c_id,"data") values(1,'hello');
insert into "data"(c_id,"data") values(2,'china');
update "data" set "data"=1000 where "data"='hello';
delete from "data" where "data"='china';
select "data" from "data" where "data"!='hello' order by "data";

drop table "data";

