--  @testpoint:openGauss关键字operator(非保留)，同时作为表名和列名带引号，并进行dml操作,operator列的值最终显示为1000

drop table if exists "operator";
create table "operator"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"operator" varchar(100) default 'operator'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "operator"(c_id,"operator") values(1,'hello');
insert into "operator"(c_id,"operator") values(2,'china');
update "operator" set "operator"=1000 where "operator"='hello';
delete from "operator" where "operator"='china';
select "operator" from "operator" where "operator"!='hello' order by "operator";

drop table "operator";

