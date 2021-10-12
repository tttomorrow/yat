-- @testpoint: jsonb额外支持操作函数：gin_compare_jsonb（比较两个键值a和b,若键值a大于b则返回正数，小于返回负数，等于返回0。当入参不合理时，合理报错）
--合理入参
select btint4cmp(gin_compare_jsonb('p',2),0);
select btint4cmp(gin_compare_jsonb('1','1'),0);
select btint4cmp(gin_compare_jsonb(1,2),0);
select btint4cmp(gin_compare_jsonb(12,'false'),0);
select btint4cmp(gin_compare_jsonb('no','true'),0);
select btint4cmp(gin_compare_jsonb('true','false'),0);
select btint4cmp(gin_compare_jsonb('p',null),0);
select btint4cmp(gin_compare_jsonb(029,'null'),0);
select btint4cmp(gin_compare_jsonb(29.0,29),0);
select btint4cmp(gin_compare_jsonb('',null),0);
select btint4cmp(gin_compare_jsonb('false',null),0);
select btint4cmp(gin_compare_jsonb('{"false":1}','{"true:0"}'),0);
select btint4cmp(gin_compare_jsonb('[{"false":1},123,"abc"]','{"false":1}'),0);

--不合理入参：报错
select gin_compare_jsonb(true,'null');
select gin_compare_jsonb(false,qqqq );
select gin_compare_jsonb(qqqq,29);
select gin_compare_jsonb(www,'null');
