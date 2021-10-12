--  @testpoint:openGauss关键字reassign(非保留)，同时作为表名和列名带引号，并进行dml操作,reassign列的值最终显示为1000

drop table if exists "reassign";
create table "reassign"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"reassign" varchar(100) default 'reassign'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "reassign"(c_id,"reassign") values(1,'hello');
insert into "reassign"(c_id,"reassign") values(2,'china');
update "reassign" set "reassign"=1000 where "reassign"='hello';
delete from "reassign" where "reassign"='china';
select "reassign" from "reassign" where "reassign"!='hello' order by "reassign";

drop table "reassign";

