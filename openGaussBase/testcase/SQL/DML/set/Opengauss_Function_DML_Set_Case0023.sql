--查询是否存在名为myschema1的模式
 select schema_name from information_schema.schemata where schema_name ='myschema1';
 --设置schema为不存在的模式myschema1，合理报错（实际未报错）
 set session current_schema to myschema1;
 --查看current_schema的值，应该是默认public（实际为空）
 select current_schema;