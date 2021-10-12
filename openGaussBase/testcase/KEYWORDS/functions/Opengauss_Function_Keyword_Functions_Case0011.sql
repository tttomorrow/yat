--  @testpoint:openGauss关键字functions(非保留)，同时作为表名和列名带引号，并进行dml操作,functions列的值最终显示为1000

drop table if exists "functions";
create table "functions"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"functions" varchar(100) default 'functions'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "functions"(c_id,"functions") values(1,'hello');
insert into "functions"(c_id,"functions") values(2,'china');
update "functions" set "functions"=1000 where "functions"='hello';
delete from "functions" where "functions"='china';
select "functions" from "functions" where "functions"!='hello' order by "functions";

drop table "functions";

