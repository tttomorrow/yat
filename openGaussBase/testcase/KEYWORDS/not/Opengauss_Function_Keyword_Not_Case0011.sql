--  @testpoint:openGauss保留关键字not同时作为表名和列名带引号，并进行dml操作,not列的值最终显示为1000
drop table if exists "not";
create table "not"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"not" varchar(100) default 'not'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入数据
insert into "not"(c_id,"not") values(1,'hello');
insert into "not"(c_id,"not") values(2,'china');

--更新表数据
update "not" set "not"=1000 where "not"='hello';

--清理表数据
delete from "not" where "not"='china';

--查看表数据
select "not" from "not" where "not"!='hello' order by "not";

--清理环境
drop table "not";