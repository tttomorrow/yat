-- @testpoint: 创建本地临时表,插入数据

drop table if exists test_json_12;
create local temporary table test_json_12 (id json) WITH (orientation=row, compression=no);
insert into test_json_12 values ('{"f1":1,"f2":true,"f3":"Hi"}');
select * from test_json_12;
drop table test_json_12;