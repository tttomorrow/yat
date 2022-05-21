--  @testpoint:openGauss关键字Index(非保留)，同时作为表名和列名带引号，并进行dml操作,Index列的值最终显示为1000

drop table if exists "Index";
create table "Index"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Index" varchar(100) default 'Index'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "Index"(c_id,"Index") values(1,'hello');
insert into "Index"(c_id,"Index") values(2,'china');
update "Index" set "Index"=1000 where "Index"='hello';
delete from "Index" where "Index"='china';
select "Index" from "Index" where "Index"!='hello' order by "Index";

drop table "Index";

