--  @testpoint:openGauss关键字dictionary(非保留)，同时作为表名和列名带引号，并进行dml操作,dictionary列的值最终显示为1000

drop table if exists "dictionary";
create table "dictionary"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"dictionary" varchar(100) default 'dictionary'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "dictionary"(c_id,"dictionary") values(1,'hello');
insert into "dictionary"(c_id,"dictionary") values(2,'china');
update "dictionary" set "dictionary"=1000 where "dictionary"='hello';
delete from "dictionary" where "dictionary"='china';
select "dictionary" from "dictionary" where "dictionary"!='hello' order by "dictionary";

drop table "dictionary";

