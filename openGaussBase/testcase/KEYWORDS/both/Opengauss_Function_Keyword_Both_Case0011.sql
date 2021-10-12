--  @testpoint:openGauss保留关键字Both同时作为表名和列名带引号，并进行dml操作,Both列的值最终显示为1000
drop table if exists "Both";
create table "Both"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Both" varchar(100) default 'Both'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入数据
insert into "Both"(c_id,"Both") values(1,'hello');
insert into "Both"(c_id,"Both") values(2,'china');

--更新表数据
update "Both" set "Both"=1000 where "Both"='hello';

--清理表数据
delete from "Both" where "Both"='china';

--查看表数据
select "Both" from "Both" where "Both"!='hello' order by "Both";

--清理环境
drop table "Both";