-- @testpoint: jsonb额外支持操作函数：jsonb_exists（字符串text是否以key\elem\scalar的形式存在JSON的顶层，同操作符 ?，当入参不合理时，合理报错）

--合理入参：存在
select jsonb_exists('"188"',188);
select jsonb_exists('{"a":1, "b":2}','b');
select jsonb_exists('["abcdefg",1,{"db":"test"},null,"true",false]','true');
select jsonb_exists('["abcdefg",138,{"db":"test"},null,"true",false]','abcdefg');
select jsonb_exists('["abcdefg","138",{"db":"test"},null,"true",false]','138');
select jsonb_exists('["abcdefg","138",{"db":"test"},"null","true",false]','null');
select jsonb_exists('["abcdefg",138,"{\"db\":\"test\"}",null,"true",false]','{"db":"test"}');
select jsonb_exists('["abcdefg",1,{"db":"test"},null,"true",false]',(select true ::text));

--合理入参：不存在
select jsonb_exists( '"188.8"','"188"');
select jsonb_exists('{"a":1, "b":2}','"ab"');
select jsonb_exists('188','(select "188" ::jsonb)');
select jsonb_exists('["abcdefg",1,{"db":"test"},null,"true",false]', ' ');
select jsonb_exists('["abcdefg",138,{"db":"test"},null,"true",false]',(select 138 ::text));
select jsonb_exists('{"db":{"test":"111"}}','{"db":"test"}');
select jsonb_exists('["abcdefg",1,{"db":"test"},null,"true",false]','(select false ::text)');

--不合理入参：报错
select jsonb_exists('{"a":1, "b":2}', (select '"b"'::jsonb));
select jsonb_exists('["abcdefg",1,{"db":"test"},null,"true",false]', (select 'true'::jsonb));
select jsonb_exists('["abcdefg",138,{"db":"test"},null,"true",false]', abcdefg);
select jsonb_exists('["abcdefg",138,"{\"db\":\"test\"}",null,"true",false]', "db");
select jsonb_exists('["abcdefg","138",{"db":"test"},"null","true",false]',(select 'true'::string));