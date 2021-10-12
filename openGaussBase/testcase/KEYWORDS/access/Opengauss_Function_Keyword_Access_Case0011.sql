--  @testpoint:openGauss关键字access(非保留)，同时作为表名和列名带引号，并进行dml操作,access列的值最终显示为1000
--创建表
drop table if exists "access";
create table "access"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"access" varchar(100) default 'access'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "access"(c_id,"access") values(1,'hello');
insert into "access"(c_id,"access") values(2,'china');

--查看表内容
select * from "access";

--更新表数据
update "access" set "access"=1000 where "access"='hello';

--删除表数据
delete from "access" where "access"='china';

--查询表内容
select "access" from "access" where "access"!='hello' order by "access";

--清理环境
drop table "access";
