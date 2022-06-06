--  @testpoint:openGauss保留关键字select同时作为表名和列名带引号，并进行dml操作,select列的值最终显示为1000
drop table if exists "select";
create table "select"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"select" varchar(100) default 'select'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);

--插入数据
insert into "select"(c_id,"select") values(1,'hello');
insert into "select"(c_id,"select") values(2,'china');

--更新表数据
update "select" set "select"=1000 where "select"='hello';

--清理表数据
delete from "select" where "select"='china';

--查看表数据
select "select" from "select" where "select"!='hello' order by "select";

--清理环境
drop table "select";