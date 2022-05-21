--  @testpoint:openGauss关键字binary_integer(非保留)，同时作为表名和列名带引号，并进行dml操作,binary_integer列的值最终显示为1000
--创建表
drop table if exists "binary_integer";
create table "binary_integer"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"binary_integer" varchar(100) default 'binary_integer'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "binary_integer"(c_id,"binary_integer") values(1,'hello');
insert into "binary_integer"(c_id,"binary_integer") values(2,'china');

--查看表内容
select * from "binary_integer";

--更新表数据
update "binary_integer" set "binary_integer"=1000 where "binary_integer"='hello';

--删除表数据
delete from "binary_integer" where "binary_integer"='china';

--查询表内容
select "binary_integer" from "binary_integer" where "binary_integer"!='hello' order by "binary_integer";

--清理环境
drop table "binary_integer";
