--  @testpoint:openGauss保留关键字do同时作为表名和列名带引号，并进行dml操作,do列的值最终显示为1000
drop table if exists "do";
create table "do"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"do" varchar(100) default 'do'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "do"(c_id,"do") values(1,'hello');
insert into "do"(c_id,"do") values(2,'china');
update "do" set "do"=1000 where "do"='hello';
delete from "do" where "do"='china';
select "do" from "do" where "do"!='hello' order by "do";

drop table "do";