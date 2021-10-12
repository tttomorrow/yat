-- @testpoint: 字节长度设定为0，合理报错

drop table if exists test_varchar2_01;
create table test_varchar2_01 (name varchar2(0));
