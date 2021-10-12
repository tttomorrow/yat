-- @testpoint: 参数为字符
select nullif('aa','aa');
select nullif('aaa','aa');
select nullif('   aa','aa');
select nullif('   aa','   aa');