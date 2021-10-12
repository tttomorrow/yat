--  @testpoint:openGauss保留关键字And同时作为表名和列名带引号，并进行dml操作,And列的值最终显示为1000
drop table if exists "And";
create table "And"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"And" varchar(100) default 'And'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入数据
insert into "And"(c_id,"And") values(1,'hello');
insert into "And"(c_id,"And") values(2,'china');

--更新表数据
update "And" set "And"=1000 where "And"='hello';

--清理表数据
delete from "And" where "And"='china';

--查看表数据
select "And" from "And" where "And"!='hello' order by "And";

--清理环境
drop table "And";