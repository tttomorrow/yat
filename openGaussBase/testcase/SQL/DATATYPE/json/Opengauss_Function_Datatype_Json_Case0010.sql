-- @testpoint: json数据类型转换至text;

drop table if exists test_json_10;
create  table test_json_10 (id json);
insert into test_json_10 values ('{"f1":1,"f2":true,"f3":"Hi"}');
alter table test_json_10 alter column id type text;
select * from test_json_10;
drop table test_json_10;