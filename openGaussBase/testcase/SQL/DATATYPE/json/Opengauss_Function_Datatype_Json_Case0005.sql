-- @testpoint: 插入非法空值,合理报错

drop table if exists test_json_05;
create table test_json_05 (c1 int,c2 json);
insert into test_json_05 values (1,' ');
drop table test_json_05;