--  @testpoint:openGauss关键字result(非保留)，同时作为表名和列名带引号，并进行dml操作,result列的值最终显示为1000

drop table if exists "result";
create table "result"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"result" varchar(100) default 'result'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "result"(c_id,"result") values(1,'hello');
insert into "result"(c_id,"result") values(2,'china');
update "result" set "result"=1000 where "result"='hello';
delete from "result" where "result"='china';
select "result" from "result" where "result"!='hello' order by "result";

drop table "result";

