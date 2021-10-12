--  @testpoint:openGauss关键字delete(非保留)，同时作为表名和列名带引号，并进行dml操作,delete列的值最终显示为1000

drop table if exists "delete";
create table "delete"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"delete" varchar(100) default 'delete'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "delete"(c_id,"delete") values(1,'hello');
insert into "delete"(c_id,"delete") values(2,'china');
update "delete" set "delete"=1000 where "delete"='hello';
delete from "delete" where "delete"='china';
select "delete" from "delete" where "delete"!='hello' order by "delete";

drop table "delete";

