-- @testpoint: 函数notlike(x bytea name text, y bytea text)，比较x和y是否不一致

--参数是正常值
select notlike(1,2);
select notlike(1,1);
--参数是字符串
select notlike('a','a');
select notlike('@','b');
select notlike('批量生成','批量生成');
