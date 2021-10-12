--  @testpoint:openGauss关键字cluster(非保留)，同时作为表名和列名带引号，并进行dml操作,cluster列的值最终显示为1000
--创建表
drop table if exists "cluster";
create table "cluster"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"cluster" varchar(100) default 'cluster'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "cluster"(c_id,"cluster") values(1,'hello');
insert into "cluster"(c_id,"cluster") values(2,'china');

--查看表内容
select * from "cluster";

--更新表数据
update "cluster" set "cluster"=1000 where "cluster"='hello';

--删除表数据
delete from "cluster" where "cluster"='china';

--查询表内容
select "cluster" from "cluster" where "cluster"!='hello' order by "cluster";

--清理环境
drop table "cluster";
