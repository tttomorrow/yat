-- @testpoint: substring函数合法值及空值测试
select substring('jjslfhaha' from 6 for 4);
select substring('jjslfhaha' from null for 4);
select substring('jjslfhaha' from 6 for null); 
select substring('jjslfhaha' from null for null);
select substring('jjslfhaha' from 0 for 6);
select substring('jjslfhaha' from -1 for 6); 
