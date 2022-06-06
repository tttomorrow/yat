--  @testpoint:openGauss关键字unlisten(非保留)，同时作为表名和列名带引号，并进行dml操作,unlisten列的值最终显示为1000

drop table if exists "unlisten" CASCADE;
create table "unlisten"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"unlisten" varchar(100) default 'unlisten'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "unlisten"(c_id,"unlisten") values(1,'hello');
insert into "unlisten"(c_id,"unlisten") values(2,'china');
update "unlisten" set "unlisten"=1000 where "unlisten"='hello';
delete from "unlisten" where "unlisten"='china';
select "unlisten" from "unlisten" where "unlisten"!='hello' order by "unlisten";

drop table "unlisten";

