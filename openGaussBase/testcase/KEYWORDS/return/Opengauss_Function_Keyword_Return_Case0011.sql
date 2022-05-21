--  @testpoint:openGauss关键字return(非保留)，同时作为表名和列名带引号，并进行dml操作,return列的值最终显示为1000

drop table if exists "return";
create table "return"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"return" varchar(100) default 'return'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "return"(c_id,"return") values(1,'hello');
insert into "return"(c_id,"return") values(2,'china');
update "return" set "return"=1000 where "return"='hello';
delete from "return" where "return"='china';
select "return" from "return" where "return"!='hello' order by "return";

drop table "return";

