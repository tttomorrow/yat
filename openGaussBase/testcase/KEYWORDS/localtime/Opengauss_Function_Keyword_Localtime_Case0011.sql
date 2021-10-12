--  @testpoint:openGauss保留关键字localtime同时作为表名和列名带引号，并进行dml操作,localtime列的值最终显示为1000
drop table if exists "localtime";
create table "localtime"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"localtime" varchar(100) default 'localtime'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入数据
insert into "localtime"(c_id,"localtime") values(1,'hello');
insert into "localtime"(c_id,"localtime") values(2,'china');

--更新表数据
update "localtime" set "localtime"=1000 where "localtime"='hello';

--清理表数据
delete from "localtime" where "localtime"='china';

--查看表数据
select "localtime" from "localtime" where "localtime"!='hello' order by "localtime";

--清理环境
drop table "localtime";