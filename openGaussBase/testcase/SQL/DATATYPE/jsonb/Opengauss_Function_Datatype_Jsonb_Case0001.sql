-- @testpoint: openGauss可否正确判断JSON类型:对象（不符合规范的合理报错）

--符合规范
select '{"name": ["john", false],  "age":    18,  "assress":  {"country" :"china", "zip-code": "10000"}, "NULL":null, "true":true}'::JSON;
select '{"name": ["john",false],"age":18,"assress":{"country" :"china", "zip-code": "10000"}, "NULL":null, "true":true}'::JSON;
--不符合规范
select '{"name": ["john", false],  "age":    18,  "assress":  {"country" :"china", "zip-code": "10000"},true:true}'::JSON;
select '{"name": ["john", "Dan"], , "age":    18,  "assress":  {"country" : "china", "zip-code": "10000"}}'::JSON;
select "{"name": ["john", false],  "age":    18,  "assress":  {"country" :"china", "zip-code": "10000"},"true":true}"::JSON;
select {"name": ["john", false],  "age":    18,  "assress":  {"country" :"china", "zip-code": "10000"},true:true}::JSON;
select '{"name","john",  "age"}'::JSON;
select "{"name","john",  "age"}"::JSON;
select '{name,john, age}'::JSON;
select "{name,john, age}"::JSON;
select '"name","john",  "age"'::JSON;