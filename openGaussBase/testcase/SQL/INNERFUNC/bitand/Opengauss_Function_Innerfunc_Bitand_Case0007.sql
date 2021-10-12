-- @testpoint: 输入参数为运算表达式

select bitand(0&3,3) & bitand(15,3) as result from sys_dummy;
select bitand(6,6&2) & bitand(15,'') as result from sys_dummy;
select bitand(13/2,(10+2)%5) & bitand(15,3) as result from sys_dummy;
