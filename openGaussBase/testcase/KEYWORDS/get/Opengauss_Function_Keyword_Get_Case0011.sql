--  @testpoint:openGauss关键字get(非保留)，同时作为表名和列名带引号，并进行dml操作,get列的值最终显示为1000

drop table if exists "get";
create table "get"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"get" varchar(100) default 'get'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "get"(c_id,"get") values(1,'hello');
insert into "get"(c_id,"get") values(2,'china');
update "get" set "get"=1000 where "get"='hello';
delete from "get" where "get"='china';
select "get" from "get" where "get"!='hello' order by "get";

drop table "get";

