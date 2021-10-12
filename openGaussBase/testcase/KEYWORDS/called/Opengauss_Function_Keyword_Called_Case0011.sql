--  @testpoint:openGauss关键字called(非保留)，同时作为表名和列名带引号，并进行dml操作,called列的值最终显示为1000
--创建表
drop table if exists "called";
create table "called"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"called" varchar(100) default 'called'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "called"(c_id,"called") values(1,'hello');
insert into "called"(c_id,"called") values(2,'china');

--查看表内容
select * from "called";

--更新表数据
update "called" set "called"=1000 where "called"='hello';

--删除表数据
delete from "called" where "called"='china';

--查询表内容
select "called" from "called" where "called"!='hello' order by "called";

--清理环境
drop table "called";
