--  @testpoint:openGauss关键字rollup(非保留)，同时作为表名和列名带引号，并进行dml操作,rollup列的值最终显示为1000
--创建表
drop table if exists "rollup";
create table "rollup"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"rollup" varchar(100) default 'rollup'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "rollup"(c_id,"rollup") values(1,'hello');
insert into "rollup"(c_id,"rollup") values(2,'china');

--查看表内容
select * from "rollup";

--更新表数据
update "rollup" set "rollup"=1000 where "rollup"='hello';

--删除表数据
delete from "rollup" where "rollup"='china';

--查询表内容
select "rollup" from "rollup" where "rollup"!='hello' order by "rollup";

--清理环境
drop table "rollup";
