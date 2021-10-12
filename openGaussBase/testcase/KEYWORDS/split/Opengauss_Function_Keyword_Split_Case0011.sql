--  @testpoint:openGauss保留关键字split同时作为表名和列名带引号，并进行dml操作,split列的值最终显示为1000
drop table if exists "split";
create table "split"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"split" varchar(100) default 'split'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "split"(c_id,"split") values(1,'hello');
insert into "split"(c_id,"split") values(2,'china');
update "split" set "split"=1000 where "split"='hello';
delete from "split" where "split"='china';
select "split" from "split" where "split"!='hello' order by "split";

drop table "split";