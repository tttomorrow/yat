-- @testpoint: json数据类型转换至tinyint,date,合理报错
-- @modified at: 2020-11-26

drop table if exists test_json_04;
create table test_json_04 (id json);
insert into test_json_04 values ('{"f1":1,"f2":true,"f3":"Hi"}');
--修改json类型为tinyint
alter table test_json_04 alter column id type tinyint;
--修改json类型为date
alter table test_json_04 alter column id type date;
select * from test_json_04;
--清理环境
drop table test_json_04;