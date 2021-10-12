-- @testpoint: 修改default 为''
drop table if exists test_modify cascade;
create table test_modify(
c_id int, c_integer integer,
c_real real,c_float float, c_cdouble binary_double,
c_decimal decimal(38), c_number number(38),c_number1 number,c_number2 number(20,10),c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
c_clob clob,
c_raw raw(20),
c_blob blob,
c_date date,
c_timestamp timestamp
);

alter table test_modify alter c_id set default '';
alter table test_modify alter c_integer set default '';
alter table test_modify alter c_real set default '';
alter table test_modify alter c_float set default '';
alter table test_modify alter c_cdouble set default '';
alter table test_modify alter c_decimal set default '';
alter table test_modify alter c_number set default '';
alter table test_modify alter c_number1 set default '';
alter table test_modify alter c_number2 set default '';
alter table test_modify alter c_numeric set default '';
alter table test_modify alter c_char set default '';
alter table test_modify alter c_varchar set default '';
alter table test_modify alter c_varchar2 set default '';
alter table test_modify alter c_clob set default '';
alter table test_modify alter c_raw set default '';
alter table test_modify alter c_blob set default '';
alter table test_modify alter c_date set default '';
alter table test_modify alter c_timestamp set default '';

drop table if exists test_modify cascade;