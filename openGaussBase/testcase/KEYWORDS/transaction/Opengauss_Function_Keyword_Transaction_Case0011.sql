--  @testpoint:openGauss关键字transaction(非保留)，同时作为表名和列名带引号，并进行dml操作,transaction列的值最终显示为1000

drop table if exists "transaction" CASCADE;
create table "transaction"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"transaction" varchar(100) default 'transaction'
)
PARTITION BY RANGE (c_integer)
(
	partition P_max values less than (maxvalue)
);



insert into "transaction"(c_id,"transaction") values(1,'hello');
insert into "transaction"(c_id,"transaction") values(2,'china');
update "transaction" set "transaction"=1000 where "transaction"='hello';
delete from "transaction" where "transaction"='china';
select "transaction" from "transaction" where "transaction"!='hello' order by "transaction";

drop table "transaction";

