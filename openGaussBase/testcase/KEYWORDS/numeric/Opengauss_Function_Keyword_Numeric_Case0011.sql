--  @testpoint:openGauss关键字numeric(非保留)，同时作为表名和列名带引号，并进行dml操作,numeric列的值最终显示为1000

drop table if exists "numeric";
create table "numeric"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"numeric" varchar(100) default 'numeric'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "numeric"(c_id,"numeric") values(1,'hello');
insert into "numeric"(c_id,"numeric") values(2,'china');
update "numeric" set "numeric"=1000 where "numeric"='hello';
delete from "numeric" where "numeric"='china';
select "numeric" from "numeric" where "numeric"!='hello' order by "numeric";

drop table "numeric";
