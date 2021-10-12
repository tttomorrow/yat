--  @testpoint:openGauss关键字sequence(非保留)，同时作为表名和列名带引号，并进行dml操作,sequence列的值最终显示为1000

drop table if exists "sequence" CASCADE;
create table "sequence"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"sequence" varchar(100) default 'sequence'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "sequence"(c_id,"sequence") values(1,'hello');
insert into "sequence"(c_id,"sequence") values(2,'china');
update "sequence" set "sequence"=1000 where "sequence"='hello';
delete from "sequence" where "sequence"='china';
select "sequence" from "sequence" where "sequence"!='hello' order by "sequence";

drop table "sequence";

