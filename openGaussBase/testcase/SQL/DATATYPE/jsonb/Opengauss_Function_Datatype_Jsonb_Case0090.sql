-- @testpoint: jsonb额外支持操作函数：jsonb_contains（判断A的顶层中是否包含B中的所有元素,同操作符 @>，当入参不合理时，合理报错）


--合理入参：存在
select jsonb_contains('"ffff"','"ffff"');
select jsonb_contains( '{"a":1 ,"test":[1,2,3], "a":2}','{"a":2 ,"test":[1,2,3], "a":2}');
select jsonb_contains( '{"a":2 ,"test":[1,2,3], "a":2}','{"a":1 ,"test":[1,2,3], "a":2}');
select jsonb_contains('123','123');
select jsonb_contains('[105.2e-3, true    ]','1.0520e-1');

--合理入参：不存在
select jsonb_contains( '{ "b":    [1,  2,3]}', '{"a":1, "b": [1,2,3]}');
select jsonb_contains( '[105.2e3, "test", {"a":1}]','["test", 1.052e5 , {"a":1},   "test"]');
select jsonb_contains( '[null,"test"]','["test"         , false,      null ]');
select jsonb_contains('{"true":1, "false":2, "null":null}','{"true ":1}');
select jsonb_contains('["", -1235e-5]','[-1.235e-2,        null]');
select jsonb_contains('true','"true"');
select jsonb_contains('{"a":1 ,"test":[1,2,3], "a":2}','{"a":2 ,"test":[1,2,3], "a":1}');

--入参不合理:报错
select jsonb_contains('{a:true}, null]', 'null');
select jsonb_contains('[{a:true}, null,123]', 'null');
select jsonb_contains('[ abc,  1]','[abcd,11]');
select jsonb_contains('ddd, 1, ddd','ddd');