-- @testpoint: DQL语法，结合create table as select distinct：多个列+null

drop table if exists all_datatype_tbl;
create table all_datatype_tbl(
c_id integer,
c_boolean boolean,
c_integer integer,
c_bigint bigint,
c_real real,
c_decimal decimal(38),
c_number number(38),
c_char char(50) default null,
c_varchar varchar(50), c_clob clob,
c_blob blob,
c_timestamp timestamp,
c_interval interval day to second);

insert into all_datatype_tbl(c_id) values(123),(456),(789),(654),(321);
insert into all_datatype_tbl(c_boolean) values(true),(false),(10),(0),(null);
insert into all_datatype_tbl(c_timestamp) values(TO_DATE('2018-06-28 13:14:15', 'YYYY-MM-DD HH24:MI:SS')),(TO_DATE('2018-JUN-28 01:14:15', 'YYYY-MON-DD HH:MI:SS')),(null);
insert into all_datatype_tbl(c_interval) values('12 12:3:4.1234'),(null);

drop table if exists datatype_tbl3;
create table datatype_tbl3 as select distinct c_id,c_char,c_interval,null add_null from all_datatype_tbl;

select * from datatype_tbl3 order by 1,2;

drop table all_datatype_tbl;
drop table datatype_tbl3;

