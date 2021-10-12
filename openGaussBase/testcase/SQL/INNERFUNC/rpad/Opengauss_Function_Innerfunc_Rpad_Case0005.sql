-- @testpoint: rpad函数入参为空值
select rpad('',10,'sdsdas') from sys_dummy;
select rpad(null,10,'sdsdas') from sys_dummy;
select rpad('aaa',10,'') from sys_dummy;
select rpad('aaa',10,null) from sys_dummy;