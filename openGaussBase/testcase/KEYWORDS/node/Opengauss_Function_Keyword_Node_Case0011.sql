--  @testpoint:openGauss关键字node(非保留)，同时作为表名和列名带引号，并进行dml操作,node列的值最终显示为1000

drop table if exists "node";
create table "node"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"node" varchar(100) default 'node'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "node"(c_id,"node") values(1,'hello');
insert into "node"(c_id,"node") values(2,'china');
update "node" set "node"=1000 where "node"='hello';
delete from "node" where "node"='china';
select "node" from "node" where "node"!='hello' order by "node";

drop table "node";

