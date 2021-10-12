--  @testpoint:删除不存在的函数，省略IF EXISTS 子句并且省略函数参数，合理报错
--从pg_proc表查询函数名是u_testfun76，该函数不存在
select proname from pg_proc where proname='u_testfun76';
--删除不存在的函数u_testfun76，合理报错
drop FUNCTION  u_testfun76;