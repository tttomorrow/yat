-- @testpoint: substring函数参数3大于length(string)-from
select substring('jjslfhaha'::text from 6 for 6) as text1;