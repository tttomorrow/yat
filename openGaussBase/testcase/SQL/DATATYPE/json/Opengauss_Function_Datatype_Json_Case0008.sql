-- @testpoint: 插入不规则数据

drop table if exists test_json_08;
create table test_json_08 (id json);
insert into test_json_08 values ('{"f1":"","f2":"","f3":"","f4":""}');
insert into test_json_08 values ('{"":1,"":true,"":"Hi","":"fffffffff-9c0b-4ef8-bb6d-6bb9bd380a11"}');
insert into test_json_08 values ('{"f1":1,"f2":true,"f3":"Hi","f4":"fffffffff-9c0b-4ef8-bb6d-6bb9bd380a11"}');
select * from test_json_08;
drop table test_json_08;