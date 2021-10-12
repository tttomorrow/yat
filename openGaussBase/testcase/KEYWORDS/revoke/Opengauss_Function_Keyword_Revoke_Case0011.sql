--  @testpoint:openGauss关键字revoke(非保留)，同时作为表名和列名带引号，并进行dml操作,revoke列的值最终显示为1000
--创建表
drop table if exists "revoke";
create table "revoke"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"revoke" varchar(100) default 'revoke'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "revoke"(c_id,"revoke") values(1,'hello');
insert into "revoke"(c_id,"revoke") values(2,'china');

--查看表内容
select * from "revoke";

--更新表数据
update "revoke" set "revoke"=1000 where "revoke"='hello';

--删除表数据
delete from "revoke" where "revoke"='china';

--查询表内容
select "revoke" from "revoke" where "revoke"!='hello' order by "revoke";

--清理环境
drop table "revoke";
