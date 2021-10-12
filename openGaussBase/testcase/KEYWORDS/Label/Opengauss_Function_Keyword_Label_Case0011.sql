--  @testpoint:openGauss关键字Label(非保留)，同时作为表名和列名带引号，并进行dml操作,Label列的值最终显示为1000

drop table if exists "Label";
create table "Label"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"Label" varchar(100) default 'Label'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "Label"(c_id,"Label") values(1,'hello');
insert into "Label"(c_id,"Label") values(2,'china');
update "Label" set "Label"=1000 where "Label"='hello';
delete from "Label" where "Label"='china';
select "Label" from "Label" where "Label"!='hello' order by "Label";

drop table "Label";

