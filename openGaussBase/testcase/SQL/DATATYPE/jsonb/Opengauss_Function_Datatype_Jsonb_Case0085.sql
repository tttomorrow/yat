-- @testpoint: json额外支持操作函数：json_object（从一个文本数组构造一个 JSON 对象，当入参不合理时，合理报错）

--合理入参
select json_object('{a,1,b,2,3,NULL,"d e f","a b c"}');
select json_object('{a,b,"a b c"}', '{a,1,1}');

--不合理入参：合理报错
select json_object('[{"a":1,"b":"foo","d":false},{"a":2,"b":"bar","c":true}]');
select json_object('{a,1,b,2,3,"d e f","a b c"}');
select json_object('{a,1,b,2,null,"a b c"}');
select json_object('{"a":1,"b":"foo","d":false}');
select json_object('[a,1,b,2,3,NULL,"d e f","a b c"]');
select json_object('[{"a":1,"b":"foo","d":false},{"a":2,"b":"bar","c":true}]');