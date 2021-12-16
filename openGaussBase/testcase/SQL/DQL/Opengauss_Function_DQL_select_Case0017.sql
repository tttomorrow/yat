-- @testpoint: DQL语法，测试count distinct：单列

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
insert into all_datatype_tbl(c_integer) values(-100),(100),(-2147483648),(2147483647),(null);
insert into all_datatype_tbl(c_bigint) values(-100),(100),(-9223372036854775808),(9223372036854775807),(null);
insert into all_datatype_tbl(c_real) values(-10.01),(10.01),(-9223372036854.775808),(9223372036.854775807),(null);
insert into all_datatype_tbl(c_decimal) values(-10.01),(10.01),(-9223372036854.775808),(9223372036.854775807),(null);
insert into all_datatype_tbl(c_char) values('abc123456789abc123456789abc123456789abc123456789'),('abc123456789abc123456789abc123456789a'),(null);
insert into all_datatype_tbl(c_varchar) values('abc123456789abc123456789abc123456789abc123456789'),('abc123456789abc123456789abc123456789a'),(null);
insert into all_datatype_tbl(c_clob) values('abc123456789abc123456789abc123456789abc123456789'),('abc123456789abc123456789abc123456789a'),(null);
insert into all_datatype_tbl(c_blob) values('1010101111111111111111111111111111111111111111'),('10101011111111111111111111111111111111111111'),(null);
insert into all_datatype_tbl(c_timestamp) values(TO_DATE('2018-06-28 13:14:15', 'YYYY-MM-DD HH24:MI:SS')),(TO_DATE('2018-JUN-28 01:14:15', 'YYYY-MON-DD HH:MI:SS')),(null);
insert into all_datatype_tbl(c_interval) values('12 12:3:4.1234'),(null);

drop table if exists datatype_tbl6;
create table datatype_tbl6 as select count(distinct c_timestamp) c_sum from all_datatype_tbl;

select * from datatype_tbl6 order by 1;

drop table all_datatype_tbl;
drop table datatype_tbl6;