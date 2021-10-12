-- @testpoint: 通用函数：json_populate_recordsetset(对array-json中的每一个object-json执行上一个函数的功能，当入参不合理时，合理报错）

--json_populate_recordsetset函数，入参合理
create type keys as(id int,name varchar);
select * from json_populate_recordset(null::keys,'[{"id":"0001","name":"wangerxiao"},{"id":"0002","name":"xiaoma"}]',true);
select * from json_populate_recordset(null::keys,'[{"id":"0001","name":"wangerxiao"}]');
select * from json_populate_recordset((3,null)::keys,'[{"idd":"0001","age":"18"},{"id":"0002","name":"xiaoma"}]',false);
select * from json_populate_recordset((1,'name')::keys,'[{"a":"blurfl","x":43.2}]');

--json_populate_recordsetset函数，入参不合理
select * from json_populate_recordset(null::key,'[{"id":"0001","name":"wangerxiao"}]',true);
select * from json_populate_recordset(true::keys,'[{"id":"0001"},{"name":"wangerxiao","age":"18"}]',false);
select * from json_populate_recordset(3::keys,'{"id":"zxc","age":"18"}',false);
select * from json_populate_recordset((1,1,null)::keys,'[{"a":"blurfl","x":43.2}]');
select * from json_populate_recordset((1,"default")::keys,'{"a":"blurfl","x":43.2}');

--返回结果类型校验：anyelement
select pg_typeof(json_populate_recordset(null::keys,'[{"id":"0001","name":"wangerxiao"},{"id":"0002","name":"xiaoma"}]',true));

--删除创建的复合类型
drop type keys cascade;