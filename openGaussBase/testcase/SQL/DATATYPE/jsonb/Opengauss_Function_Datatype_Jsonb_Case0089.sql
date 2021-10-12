-- @testpoint: jsonb额外支持操作函数：jsonb_contained（判断A的所有元素是否在B的顶层中存在,同操作符 <@,当入参不合理时，合理报错）

--合理入参：存在
select jsonb_contained('"ffff"','"ffff"');
select jsonb_contained( '{ "b":    [1,  2,3]}', '{"a":1, "b": [1,2,3]}');
select jsonb_contained( '{"a":1 ,"test":[1,2,3], "a":2}','{"a":2 ,"test":[1,2,3], "a":2}');
select jsonb_contained( 'null','');
select jsonb_contained( '[105.2e3, "test", {"a":1}]','["test", 1.052e5 , {"a":1},   "test"]');
select jsonb_contained( '[null,"test"]','["test"         , false,      null ]');
select jsonb_contained( '{"a":2 ,"test":[1,2,3], "a":2}','{"a":1 ,"test":[1,2,3], "a":2}');

--合理入参：不存在
select jsonb_contained('"ffff"','"ffff    "');
select jsonb_contained('{"true":1, "false":2, "null":null}','{"true ":1}');
select jsonb_contained('["", -1235e-5]','[-1.235e-2,        null]');
select jsonb_contained('123','123');
select jsonb_contained('true','"true"');
select jsonb_contained('[105.2e-3, true    ]','1.0520e-1');
select jsonb_contained('{"a":1 ,"test":[1,2,3], "a":2}','{"a":2 ,"test":[1,2,3], "a":1}');

--入参不合理：报错
select jsonb_contained('{a:true}, null]', 'null');
select jsonb_contained('[{a:true}, null,123]', 'null');
select jsonb_contained('[ abc,  1]','[abcd,11]');
select jsonb_contained('ddd, 1, ddd','ddd');
