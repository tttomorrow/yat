--  @testpoint:openGauss保留关键字current_role同时作为表名和列名带引号，并进行dml操作,current_role列的值最终显示为1000
drop table if exists "current_role";
create table "current_role"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"current_role" varchar(100) default 'current_role'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--插入数据
insert into "current_role"(c_id,"current_role") values(1,'hello');
insert into "current_role"(c_id,"current_role") values(2,'china');

--更新表数据
update "current_role" set "current_role"=1000 where "current_role"='hello';

--清理表数据
delete from "current_role" where "current_role"='china';

--查看表数据
select "current_role" from "current_role" where "current_role"!='hello' order by "current_role";

--清理环境
drop table "current_role";