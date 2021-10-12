-- @testpoint: jsonb额外支持操作函数：jsonb_exists_all（同操作符 ?&，当入参不合理时，合理报错）
--字符串数组text[]里面，是否所有的元素，都在JSON的顶层以key\elem\scalar的形式存在，

--合理入参：存在
select jsonb_exists_all('"str"',array['str']);
select jsonb_exists_all('"null"',array['null']);
select jsonb_exists_all('{"a":1, "b": [1,2,3],"c":{"b":"d"}}',array['a','b','c']);
select jsonb_exists_all('{"a":1, "b": [1,2,3],"c":{"b":"d"}}',array['b','c']);
select jsonb_exists_all('[null, false, "123",{"a":true},"test"]',array['test','123']);

--合理入参：不存在
select jsonb_exists_all('null',array['null']);
select jsonb_exists_all('false',array['false']);
select jsonb_exists_all('true',array['true']);
select jsonb_exists_all('{"a":1, "b": [1,2,3],"c":{"b":"d"}}',array['c','d']);
select jsonb_exists_all('[null, false, 123,{"a":true},"test"]',array['123','a']);
select jsonb_exists_all('[null, false, 123,{"a":true},"test"]',array['{"a":true}']);
select jsonb_exists_all('105.2e3',array['105200']);
select jsonb_exists_all('[{"a":true}, null]',array['b','null']);

--不合理入参：报错
select jsonb_exists_all('{"a":1, "b": [10,2,3],"c":{"b":"d"}}',(select 'b'::jsonb));
select jsonb_exists_all('{"a":1, "b": [1,2,3],"c":{"b":"d"}}','{'b','d'}');
select jsonb_exists_all('[null, false, 123,{"a":true},"test"]',array'[123,'{a}']');
select jsonb_exists_all('[null, false, 123,{"a":true},"test"]',array['test',123]);
select jsonb_exists_all('105.2e3','105200');