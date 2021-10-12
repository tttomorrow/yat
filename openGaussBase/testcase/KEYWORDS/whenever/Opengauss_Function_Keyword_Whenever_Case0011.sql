--  @testpoint:openGauss关键字whenever(非保留)，同时作为表名和列名带引号，并进行dml操作,whenever列的值最终显示为1000

drop table if exists "whenever";
create table "whenever"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"whenever" varchar(100) default 'whenever'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "whenever"(c_id,"whenever") values(1,'hello');
insert into "whenever"(c_id,"whenever") values(2,'china');
update "whenever" set "whenever"=1000 where "whenever"='hello';
delete from "whenever" where "whenever"='china';
select "whenever" from "whenever" where "whenever"!='hello' order by "whenever";

drop table "whenever";

