-- @testpoint: 创建普通行存表，插入数据

drop table if exists test_json_01;
create table test_json_01 (id json) WITH (orientation=row, compression=no);
insert into test_json_01 values ('{"f1":1,"f2":true,"f3":"Hi"}');
select * from test_json_01;
drop table test_json_01;