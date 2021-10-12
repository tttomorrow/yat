-- @testpoint: 词汇可以用一个或多个权字母来标记，这些权字母限制这次词汇只能与带有匹配权的tsvector词汇进行匹配

select 'fat:ab & cat'::tsquery;
select 'super:*'::tsquery;
