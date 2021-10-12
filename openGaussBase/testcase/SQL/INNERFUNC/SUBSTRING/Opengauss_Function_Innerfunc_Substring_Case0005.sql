-- @testpoint: substring函数参数缺少测试，合理报错
select substring('jjslfhaha') as text1;
select substring('jjslfhaha' for 4) as text1;
select substring('jjslfhaha' from 4) as text1;
select substring(from 4 for 4) as text1;
select substring() as text1;
