-- @testpoint: 字符处理函数length输入参数为比较表达式
select length('345763243135689708-90897865432134215637890-=6-098765430-0897865432') from sys_dummy;
select length('1>2') from sys_dummy;
