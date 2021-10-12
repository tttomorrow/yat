-- @testpoint: regexp_matches函数模式不包含圆括号子表达式
select regexp_matches('foobarbequebaz', 'bar');