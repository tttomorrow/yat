-- @testpoint: NVARCHAR(n)操作符测试

--step1:操作符>; expect:成功
select '!'::nvarchar > '"'::nvarchar;
select '('::nvarchar > ')'::nvarchar;
select '0'::nvarchar > '5'::nvarchar;
select '0'::nvarchar > 'A'::nvarchar;
select '@'::nvarchar > 'a'::nvarchar;
select '\\'::nvarchar > 'a'::nvarchar;
select '\\'::nvarchar > 'A'::nvarchar;
select '}'::nvarchar > '~'::nvarchar;
select '}'::nvarchar > '测试'::nvarchar;
select '测试工作'::nvarchar > '测试'::nvarchar;
select '测试'::nvarchar > '测试工作'::nvarchar;
select 'aaa'::nvarchar > '测试工作'::nvarchar;
select 'aaa'::nvarchar > 'bbb'::nvarchar;

--step2:操作符>=; expect:成功
select '!'::nvarchar >= '"'::nvarchar;
select '('::nvarchar >= ')'::nvarchar;
select '0'::nvarchar >= '5'::nvarchar;
select '0'::nvarchar >= 'A'::nvarchar;
select '@'::nvarchar >= 'a'::nvarchar;
select '\\'::nvarchar >= 'a'::nvarchar;
select '\\'::nvarchar >= 'A'::nvarchar;
select '}'::nvarchar >= '~'::nvarchar;
select '}'::nvarchar >= '测试'::nvarchar;
select '测试工作'::nvarchar >= '测试'::nvarchar;
select '测试'::nvarchar >= '测试工作'::nvarchar;
select 'aaa'::nvarchar >= '测试工作'::nvarchar;
select 'aaa'::nvarchar >= 'bbb'::nvarchar;

--step3:操作符<; expect:成功
select '!'::nvarchar < '"'::nvarchar;
select '('::nvarchar < ')'::nvarchar;
select '0'::nvarchar < '5'::nvarchar;
select '0'::nvarchar < 'A'::nvarchar;
select '@'::nvarchar < 'a'::nvarchar;
select '\\'::nvarchar < 'a'::nvarchar;
select '\\'::nvarchar < 'A'::nvarchar;
select '}'::nvarchar < '~'::nvarchar;
select '}'::nvarchar < '测试'::nvarchar;
select '测试工作'::nvarchar < '测试'::nvarchar;
select '测试'::nvarchar < '测试工作'::nvarchar;
select 'aaa'::nvarchar < '测试工作'::nvarchar;
select 'aaa'::nvarchar < 'bbb'::nvarchar;

--step4:操作符<=; expect:成功
select '!'::nvarchar <= '"'::nvarchar;
select '('::nvarchar <= ')'::nvarchar;
select '0'::nvarchar <= '5'::nvarchar;
select '0'::nvarchar <= 'A'::nvarchar;
select '@'::nvarchar <= 'a'::nvarchar;
select '\\'::nvarchar <= 'a'::nvarchar;
select '\\'::nvarchar <= 'A'::nvarchar;
select '}'::nvarchar <= '~'::nvarchar;
select '}'::nvarchar <= '测试'::nvarchar;
select '测试工作'::nvarchar <= '测试'::nvarchar;
select '测试'::nvarchar <= '测试工作'::nvarchar;
select 'aaa'::nvarchar <= '测试工作'::nvarchar;
select 'aaa'::nvarchar <= 'bbb'::nvarchar;

--step5:操作符=; expect:成功
select '!'::nvarchar = '"'::nvarchar;
select '('::nvarchar = ')'::nvarchar;
select '0'::nvarchar = '5'::nvarchar;
select '0'::nvarchar = 'A'::nvarchar;
select '@'::nvarchar = 'a'::nvarchar;
select '\\'::nvarchar = 'a'::nvarchar;
select '\\'::nvarchar = 'A'::nvarchar;
select '}'::nvarchar = '~'::nvarchar;
select '}'::nvarchar = '测试'::nvarchar;
select '测试工作'::nvarchar = '测试'::nvarchar;
select '测试'::nvarchar = '测试工作'::nvarchar;
select 'aaa'::nvarchar = '测试工作'::nvarchar;
select 'aaa'::nvarchar = 'bbb'::nvarchar;

--step6:操作符<>; expect:成功
select '!'::nvarchar <> '"'::nvarchar;
select '('::nvarchar <> ')'::nvarchar;
select '0'::nvarchar <> '5'::nvarchar;
select '0'::nvarchar <> 'A'::nvarchar;
select '@'::nvarchar <> 'a'::nvarchar;
select '\\'::nvarchar <> 'a'::nvarchar;
select '\\'::nvarchar <> 'A'::nvarchar;
select '}'::nvarchar <> '~'::nvarchar;
select '}'::nvarchar <> '测试'::nvarchar;
select '测试工作'::nvarchar <> '测试'::nvarchar;
select '测试'::nvarchar <> '测试工作'::nvarchar;
select 'aaa'::nvarchar <> '测试工作'::nvarchar;
select 'aaa'::nvarchar <> 'bbb'::nvarchar;