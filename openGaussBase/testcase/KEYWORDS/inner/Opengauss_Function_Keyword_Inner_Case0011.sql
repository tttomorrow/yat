--  @testpoint:openGauss保留关键字inner同时作为表名和列名带引号，并进行dml操作,inner列的值最终显示为1000
drop table if exists "inner";
create table "inner"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"inner" varchar(100) default 'inner'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入数据
insert into "inner"(c_id,"inner") values(1,'hello');
insert into "inner"(c_id,"inner") values(2,'china');

--更新表数据
update "inner" set "inner"=1000 where "inner"='hello';

--清理表数据
delete from "inner" where "inner"='china';

--查看表数据
select "inner" from "inner" where "inner"!='hello' order by "inner";

--清理环境
drop table "inner";