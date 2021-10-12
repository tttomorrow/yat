--  @testpoint:openGauss关键字cache(非保留)，同时作为表名和列名带引号，并进行dml操作,cache列的值最终显示为1000
--创建表
drop table if exists "cache";
create table "cache"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"cache" varchar(100) default 'cache'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "cache"(c_id,"cache") values(1,'hello');
insert into "cache"(c_id,"cache") values(2,'china');

--查看表内容
select * from "cache";

--更新表数据
update "cache" set "cache"=1000 where "cache"='hello';

--删除表数据
delete from "cache" where "cache"='china';

--查询表内容
select "cache" from "cache" where "cache"!='hello' order by "cache";

--清理环境
drop table "cache";