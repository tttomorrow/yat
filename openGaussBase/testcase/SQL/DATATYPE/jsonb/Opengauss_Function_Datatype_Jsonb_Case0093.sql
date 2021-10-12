-- @testpoint: jsonb额外支持操作函数：jsonb_exists_any（字符串数组text[]里面，是否任意的元素在JSON的顶层以key\elem\scalar的形式存在，同操作符?\，当入参不合理时，合理报错）

--合理入参：存在
select jsonb_exists_any('"str"',array['str']);
select jsonb_exists_any('"null"', array['null']);
select jsonb_exists_any('{"a":1, "b": [1,2,3],"c":{"b":"d"}}',array['a','b''c']);
select jsonb_exists_any('["abcdefg",138,{"db":"test"},null,"true",false]',array['abcdefg']);
select jsonb_exists_any('["abcdefg","138",{"db":"test"},null,"true",false]',array['abcdefg','138']);
select jsonb_exists_any('[null, false, 123,{"a":true},"test"]',array['test','123']);
select jsonb_exists_any('["abcdefg",1,{"db":"test"},null,"true",false]',array(select true ::text));
select jsonb_exists_any('"null"', array['null']);
select jsonb_exists_any('{"a":1, "b": [1,2,3],"c":{"b":"d"}}', array['a','b''c']);
select jsonb_exists_any('{"a":1, "b": [1,2,3],"c":{"b":"d"}}', array['b','c']);

--合理入参：不存在
select jsonb_exists_any('null', array['null']);
select jsonb_exists_any('false', array['false']);
select jsonb_exists_any('true', array['true']);
select jsonb_exists_any('{"a":1, "b": [1,2,3],"c":{"b":"d"}}', array['d']);
select jsonb_exists_any('[null, false, 123,{"a":true},"test"]', array['123','a']);
select jsonb_exists_any('[null, false, 123,{"a":true},"test"]', array['{"a":true}']);
select jsonb_exists_any('105.2e3',array['105200']);
select jsonb_exists_any('[{"a":true}, null] ', array['b','null']);

--不合理入参：报错
select jsonb_exists_any('{"a":1, "b": [1,2,3],"c":{"b":"d"}}', array[{'c':'b'}]);
select jsonb_exists_any('{"a":1, "b":2}', (select '"b"'::jsonb));
select jsonb_exists_any('["abcdefg",1,{"db":"test"},null,"true",false]', (select 'true'::jsonb));
select jsonb_exists_any('["abcdefg",138,{"db":"test"},null,"true",false]', abcdefg);
select jsonb_exists_any('["abcdefg",138,"{\"db\":\"test\"}",null,"true",false]', "db");
select jsonb_exists_any('["abcdefg",138,"{\"db\":\"test\"}",null,"true",false]',array{"db":"test"});
select jsonb_exists_any('["abcdefg",138,"{\"db\":\"test\"}",null,"true",false]',array[{'db':'test'}]);
select jsonb_exists_any('["abcdefg","138",{"db":"test"},"null","true",false]',(select 'true'::string));