-- @testpoint: 通用函数：jsonb_populate_record(将object-json里的键值对按照键填充到一行，当入参不合理时，合理报错）

--jsonb_object_keys函数，入参合理
create type keys as(id int,name varchar);
select * from jsonb_populate_record(null::keys,'{"id":"0001","name":"wangerxiao","id":"0002","name":"xiaoma"}',true);
select * from jsonb_populate_record(null::keys,'{"id":"0001","na":"wangerxiao"}');
select * from jsonb_populate_record((3,null)::keys,'{"idd":"0001","age":"18"}',false);
select * from jsonb_populate_record((1,'name')::keys,'{"a":"blurfl","x":43.2}');

--jsonb_object_keys函数，入参不合理
select * from jsonb_populate_record(null::key,'{"id":"0001","name":"wangerxiao"}',true);
select * from jsonb_populate_record(true::keys,'{"id":"0001","name":"wangerxiao","age":"18"}',false);
select * from jsonb_populate_record(3::keys,'{"id":"zxc","age":"18"}',false);
select * from jsonb_populate_record((1,1,null)::keys,'{"a":"blurfl","x":43.2}');
select * from jsonb_populate_record((1,"default")::keys,'{"a":"blurfl","x":43.2}');

--返回结果类型校验：anyelement
select pg_typeof(jsonb_populate_record(null::keys,'{"id":"0001","name":"wangerxiao"}'));

--删除创建的复合类型
drop type keys cascade;