-- @testpoint: 插入其他类型，合理报错

drop table if exists test_json_07;
create  table test_json_07 (id json);
insert into test_json_07 values ('test');
insert into test_json_07 values (10000);
insert into test_json_07 values (100.999);
insert into test_json_07 values (date'2020-02-02');
insert into test_json_07 values (TRUE);
insert into test_json_07 values (HEXTORAW('DEADBEEF'));
drop table  test_json_07;