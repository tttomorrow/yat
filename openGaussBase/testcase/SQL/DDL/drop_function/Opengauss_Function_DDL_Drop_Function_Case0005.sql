--  @testpoint:删除不存在的函数添加IF EXISTS 子句并且省略函数参数，发出一个notice提示
--从pg_proc表查询函数名是u_testfun99
select proname from pg_proc where proname='u_testfun99';
--删除不存在的函数u_testfun99
drop FUNCTION if EXISTS u_testfun99;