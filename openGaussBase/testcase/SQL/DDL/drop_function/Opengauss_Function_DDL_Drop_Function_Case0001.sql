--  @testpoint:删除不存在的函数添加IF EXISTS 子句并且添加函数参数，发出一个notice提示
--从pg_proc表查询函数名是u_testfun66，该函数不存在
select proname from pg_proc where proname='u_testfun66';
--删除不存在的函数u_testfun66
drop FUNCTION if EXISTS u_testfun66(c_int int);