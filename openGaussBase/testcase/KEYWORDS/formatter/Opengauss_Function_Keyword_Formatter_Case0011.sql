--  @testpoint:openGauss关键字formatter(非保留)，同时作为表名和列名带引号，并进行dml操作,formatter列的值最终显示为1000

drop table if exists "formatter";
create table "formatter"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"formatter" varchar(100) default 'formatter'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "formatter"(c_id,"formatter") values(1,'hello');
insert into "formatter"(c_id,"formatter") values(2,'china');
update "formatter" set "formatter"=1000 where "formatter"='hello';
delete from "formatter" where "formatter"='china';
select "formatter" from "formatter" where "formatter"!='hello' order by "formatter";

drop table "formatter";

