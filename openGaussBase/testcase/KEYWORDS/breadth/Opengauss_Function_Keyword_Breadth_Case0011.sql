--  @testpoint:openGauss关键字breadth(非保留)，同时作为表名和列名带引号，并进行dml操作,breadth列的值最终显示为1000
--创建表
drop table if exists "breadth";
create table "breadth"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"breadth" varchar(100) default 'breadth'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "breadth"(c_id,"breadth") values(1,'hello');
insert into "breadth"(c_id,"breadth") values(2,'china');

--查看表内容
select * from "breadth";

--更新表数据
update "breadth" set "breadth"=1000 where "breadth"='hello';

--删除表数据
delete from "breadth" where "breadth"='china';

--查询表内容
select "breadth" from "breadth" where "breadth"!='hello' order by "breadth";

--清理环境
drop table "breadth";