-- @testpoint: openGauss可否正确判断JSON类型:数组（不符合规范的合理报错）

--符合规范
select '["www@13^", 1, {"name": "john"}, "2", []]'::JSON;
select '["www@13^", 1, {"name": "john"}, "2", " ",true,"null"]'::JSON;
--不符合规范
select '["name": ["john", false],  "age"，18,  "assress":  {"country" :"china", "zip-code": "10000"}, "NULL"，null, "true",true]'::JSON;
select '"www@13^", 1, {"name": "john"}, "2", " ",true,"null"'::JSON;
select '{"www@13^", 1, {"name": "john"}, "2", " ",true,"null"}'::JSON;
select ["www@13^", 1, {"name": "john"}, "2", " ",true,"null"]::JSON;
select '["www@13^", 1, {"name": "john"}, '2',,true,"null"]'::JSON;