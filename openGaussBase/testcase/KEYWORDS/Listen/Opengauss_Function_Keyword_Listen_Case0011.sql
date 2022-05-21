--  @testpoint:openGauss关键字Listen(非保留)，同时作为表名和列名带引号，并进行dml操作,Listen列的值最终显示为1000

drop table if exists "Listen";
create table "Listen"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Listen" varchar(100) default 'Listen'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "Listen"(c_id,"Listen") values(1,'hello');
insert into "Listen"(c_id,"Listen") values(2,'china');
update "Listen" set "Listen"=1000 where "Listen"='hello';
delete from "Listen" where "Listen"='china';
select "Listen" from "Listen" where "Listen"!='hello' order by "Listen";

drop table "Listen";

