--  @testpoint:openGauss保留关键字returning同时作为表名和列名带引号，并进行dml操作,returning列的值最终显示为1000
drop table if exists "returning";
create table "returning"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"returning" varchar(100) default 'returning'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入数据
insert into "returning"(c_id,"returning") values(1,'hello');
insert into "returning"(c_id,"returning") values(2,'china');

--更新表数据
update "returning" set "returning"=1000 where "returning"='hello';

--清理表数据
delete from "returning" where "returning"='china';

--查看表数据
select "returning" from "returning" where "returning"!='hello' order by "returning";

--清理环境
drop table "returning";