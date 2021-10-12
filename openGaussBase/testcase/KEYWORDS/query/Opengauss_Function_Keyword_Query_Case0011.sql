--  @testpoint:openGauss关键字query(非保留)，同时作为表名和列名带引号，并进行dml操作,query列的值最终显示为1000

drop table if exists "query";
create table "query"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"query" varchar(100) default 'query'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "query"(c_id,"query") values(1,'hello');
insert into "query"(c_id,"query") values(2,'china');
update "query" set "query"=1000 where "query"='hello';
delete from "query" where "query"='china';
select "query" from "query" where "query"!='hello' order by "query";

drop table "query";

