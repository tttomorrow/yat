--  @testpoint:事务中使用set local命令设置xml解析方式
--开启事务
start transaction;
--set local命令设置xml解析方式
set local xml option document;
--查看解析方式更改为document
show xmloption;
--提交事务
commit;
--查看xml解析方式，恢复为默认content
show xmloption;

--再次开启事务
start transaction;
--set local命令设置xml解析方式
set local xml option document;
--查看解析方式更改为document
show xmloption;
--回滚
rollback;
--查看xml解析方式，恢复为默认content
show xmloption;