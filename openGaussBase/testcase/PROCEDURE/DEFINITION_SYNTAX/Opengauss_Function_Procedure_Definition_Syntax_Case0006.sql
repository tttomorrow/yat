-- @testpoint: 存储过程声明语法带 定义变量 INTEGER
--前置条件
drop table if exists table_pro_006;
create table table_pro_006(id int,name varchar2(20));
insert into table_pro_006 values (1,'李明'),(2,'李华'),(3,'张三');

--创建存储过程
DROP PROCEDURE if exists Proc_Syntax_006;
CREATE OR REPLACE PROCEDURE Proc_Syntax_006(IN name1 varchar2(20))
IS
DECLARE
emp_id  INTEGER := 7788;
begin
emp_id := 5*7784;
raise info ':%',emp_id;
end;
/

--调用存储过程
call Proc_Syntax_006('李华');

--清理环境
DROP PROCEDURE  Proc_Syntax_006;
drop table table_pro_006;