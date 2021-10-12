--  @testpoint:openGauss关键字returned_length(非保留)，同时作为表名和列名带引号，并进行dml操作,returned_length列的值最终显示为1000

drop table if exists "returned_length";
create table "returned_length"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"returned_length" varchar(100) default 'returned_length'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "returned_length"(c_id,"returned_length") values(1,'hello');
insert into "returned_length"(c_id,"returned_length") values(2,'china');
update "returned_length" set "returned_length"=1000 where "returned_length"='hello';
delete from "returned_length" where "returned_length"='china';
select "returned_length" from "returned_length" where "returned_length"!='hello' order by "returned_length";

drop table "returned_length";

