-- @testpoint: 测试create table as select distinct：嵌套查询

drop table if exists all_datatype_tbl01;
drop table if exists all_datatype_tbl02;
create table all_datatype_tbl01(c_id integer,c_boolean boolean,c_integer integer,c_bigint bigint);
create table all_datatype_tbl02(c_id integer,c_boolean boolean,c_integer integer,c_bigint bigint);

insert into all_datatype_tbl01(c_id) values(123),(456),(789),(654),(321);
insert into all_datatype_tbl01(c_boolean) values(true),(false),(10),(0),(null);
insert into all_datatype_tbl01(c_integer) values(-100),(100),(-2147483648),(2147483647),(null);
insert into all_datatype_tbl01(c_bigint) values(-100),(100),(-9223372036854775808),(9223372036854775807),(null);

insert into all_datatype_tbl02(c_id) values(1234),(456),(789),(654),(4321);
insert into all_datatype_tbl02(c_boolean) values(true),(false),('yes'),('no'),(null);
insert into all_datatype_tbl02(c_integer) values(-100),(100),(-214),(214),(null);
insert into all_datatype_tbl02(c_bigint) values(-100),(100),(-922),(922),(null);

drop table if exists datatype_tbl5;
create table datatype_tbl5 as select distinct * from (select c_boolean,c_bigint,null null_add1 from all_datatype_tbl01 union select c_boolean,c_bigint,null null_add2 from all_datatype_tbl02);

select * from datatype_tbl5 order by 1,2;

drop table all_datatype_tbl01;
drop table all_datatype_tbl02;
drop table datatype_tbl5;


