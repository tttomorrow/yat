--  @testpoint:openGauss关键字absolute(非保留)，同时作为表名和列名带引号，并进行dml操作,absolute列的值最终显示为1000
--创建表
drop table if exists "absolute";
create table "absolute"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"absolute" varchar(100) default 'absolute'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "absolute"(c_id,"absolute") values(1,'hello');
insert into "absolute"(c_id,"absolute") values(2,'china');

--查看表内容
select * from "absolute";

--更新表数据
update "absolute" set "absolute"=1000 where "absolute"='hello';

--删除表数据
delete from "absolute" where "absolute"='china';

--查询表内容
select "absolute" from "absolute" where "absolute"!='hello' order by "absolute";

--清理环境
drop table "absolute";
