--  @testpoint:openGauss关键字matched(非保留)，同时作为表名和列名带引号，并进行dml操作,matched列的值最终显示为1000

drop table if exists "matched";
create table "matched"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"matched" varchar(100) default 'matched'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "matched"(c_id,"matched") values(1,'hello');
insert into "matched"(c_id,"matched") values(2,'china');
update "matched" set "matched"=1000 where "matched"='hello';
delete from "matched" where "matched"='china';
select "matched" from "matched" where "matched"!='hello' order by "matched";

drop table "matched";

