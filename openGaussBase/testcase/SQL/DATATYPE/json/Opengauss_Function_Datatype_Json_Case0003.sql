-- @testpoint: json数据类型转换至varchar2,char
-- @modified at: 2020-11-26

drop table if exists test_json_03;
create table test_json_03 (id json);
insert into test_json_03 values ('{"f1":1,"f2":true,"f3":"Hi"}');
--修改json类型为varchar2
alter table test_json_03 alter column id TYPE VARCHAR2(200);
--查询字段信息是否修改成功
select format_type(a.atttypid,a.atttypmod) as type from pg_class as c,pg_attribute as a where c.relname = 'test_json_03' and a.attrelid = c.oid and a.attnum>0;
select * from test_json_03;

drop table if exists test_json_03;
create table test_json_03 (id json);
--修改json字段类型为char
alter table test_json_03 alter column id type char(100);
--查询字段信息是否修改成功
select format_type(a.atttypid,a.atttypmod) as type from pg_class as c,pg_attribute as a where c.relname = 'test_json_03' and a.attrelid = c.oid and a.attnum>0;
--清理环境
drop table test_json_03;