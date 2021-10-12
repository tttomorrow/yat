-- @testpoint: 插入空值

drop table if exists test_json_06;
create table test_json_06 (id json);
insert into test_json_06 values (null);
insert into test_json_06 values ('');
drop table test_json_06;