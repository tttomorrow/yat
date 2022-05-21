--  @testpoint:openGauss关键字call(非保留)，同时作为表名和列名带引号，并进行dml操作,call列的值最终显示为1000
--创建表
drop table if exists "call";
create table "call"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"call" varchar(100) default 'call'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "call"(c_id,"call") values(1,'hello');
insert into "call"(c_id,"call") values(2,'china');

--查看表内容
select * from "call";

--更新表数据
update "call" set "call"=1000 where "call"='hello';

--删除表数据
delete from "call" where "call"='china';

--查询表内容
select "call" from "call" where "call"!='hello' order by "call";

--清理环境
drop table "call";
