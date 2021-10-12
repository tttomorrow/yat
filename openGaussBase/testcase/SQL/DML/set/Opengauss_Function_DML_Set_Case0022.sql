--查询是否存在名为myschema1的模式
 select schema_name from information_schema.schemata where schema_name ='myschema1';
 --设置schema为不存在的schema，合理报错
 set session SCHEMA 'myschema1';
 --查看current_schema的值，还是默认public，实际默认schema变为空
 select current_schema;

