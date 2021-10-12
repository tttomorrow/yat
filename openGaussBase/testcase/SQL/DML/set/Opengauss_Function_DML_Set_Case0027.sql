--查询是否存在模式名为myschema1
select * from information_schema.schemata where schema_name='myschema1';
--set local to命令设置schema为不存在myschema1，合理报错（实际未报错）
set local current_schema to myschema1;
--查询当前schema，还是public
select current_schema;
--set local =命令设置schema为不存在myschema1，合理报错（实际未报错）
set local current_schema to myschema1;
--查询当前schema，还是public
select current_schema;