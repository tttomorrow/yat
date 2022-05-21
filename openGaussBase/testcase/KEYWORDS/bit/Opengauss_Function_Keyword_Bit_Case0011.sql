--  @testpoint:openGauss关键字bit(非保留)，同时作为表名和列名带引号，并进行dml操作,bit列的值最终显示为1000
--创建表
drop table if exists "bit";
create table "bit"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"bit" varchar(100) default 'bit'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--向表中插入数据
insert into "bit"(c_id,"bit") values(1,'hello');
insert into "bit"(c_id,"bit") values(2,'china');

--查看表内容
select * from "bit";

--更新表数据
update "bit" set "bit"=1000 where "bit"='hello';

--删除表数据
delete from "bit" where "bit"='china';

--查询表内容
select "bit" from "bit" where "bit"!='hello' order by "bit";

--清理环境
drop table "bit";
