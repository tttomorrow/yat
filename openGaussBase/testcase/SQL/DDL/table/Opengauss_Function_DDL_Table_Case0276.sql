-- @testpoint: 修改default的值

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

-- @testpoint: 输入非空数据，修改default 为null
insert into test_modify values(1,1,1,1,1,1,1,1,1,1,1,1,1,'1','1','1',sysdate,sysdate);

--alter table test_modify MODIFY (c_id default null, c_integer default null,c_real default null,c_float default null, c_cdouble  default null,c_decimal  default null, c_number default null,c_number1  default null,c_number2  default null,c_numeric  default null,c_char default null, c_varchar default null, c_varchar2  default null,c_raw default null,c_date  default null,c_timestamp  default null,c_clob  default null,c_blob default null);

--alter table test_modify MODIFY c_id default null;
alter table test_modify alter c_id set default null;
alter table test_modify alter c_integer set default null;
alter table test_modify alter c_real set default null;
alter table test_modify alter c_float set default null;
alter table test_modify alter c_cdouble set default null;
alter table test_modify alter c_decimal set default null;
alter table test_modify alter c_number set default null;
alter table test_modify alter c_number1 set default null;
alter table test_modify alter c_number2 set default null;
alter table test_modify alter c_numeric set default null;
alter table test_modify alter c_char set default null;
alter table test_modify alter c_varchar set default null;
alter table test_modify alter c_varchar2 set default null;
alter table test_modify alter c_clob set default null;
alter table test_modify alter c_raw set default null;
alter table test_modify alter c_blob set default null;
alter table test_modify alter c_date set default null;
alter table test_modify alter c_timestamp set default null;

drop table if exists test_modify cascade;