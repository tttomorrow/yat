-- @testpoint: json额外支持操作函数：json_build_array（从一个可变参数列表构造出一个JSON数组，当入参不合理时，合理报错）

--合理入参
select json_build_array('a',1,'b',1.2,'c',true,'d',null,'e',json '{"x": 3, "y": [1,2,3]}','');
select json_build_array('a',1,'b',1.2,'c',true,'d',null,'e','{"x": 3, "y": [1,2,3]}','false');
select json_build_array('[1,"b",1.2,"c",true,"d"]',null,'1236.8','{"x": 3, "y": [1,2,3]}','null');
select json_build_array(json'[1,"b",1.2,"c",true,"d"]',null,'1236.8','{"x": 3, "y": [1,2,3]}','');

--不合理入参
select json_build_array('a',1,'b',1.2,'c','true','d',"null",'1236.8','{"x": 3, "y": [1,2,3]}','');
select json_build_array('a',1,'b',1.2,'c',"true",'d','null','1236.8','{"x": 3, "y": [1,2,3]}','');
select json_build_array(1,json'b','[1.2,"c",true,"d"]',null,'+1236.8','{"x": 3, "y": [1,2,3]}','');
select json_build_array(1,'b','[1.2,"c",true,"d"]',null,json'+1236.8','{"x": 3, "y": [1,2,3]}','');

--返回结果类型校验：Array-json
select pg_typeof(json_build_array('a',1,'b',1.2,'c',true,'d',null,'e',json '{"x": 3, "y": [1,2,3]}',''));