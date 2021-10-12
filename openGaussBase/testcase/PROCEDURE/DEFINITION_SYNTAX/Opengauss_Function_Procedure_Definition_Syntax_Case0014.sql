-- @testpoint: 存储过程声明语法带IN模式的存储过程 IN可以省略

--前置条件
drop table if exists table_pro_014;
create table table_pro_014(id int,name varchar2(20));
insert into table_pro_014 values (1,'李明'),(2,'李华'),(3,'张三');

--创建存储过程
CREATE OR REPLACE PROCEDURE Proc_Syntax_014(name1 varchar2(20))  IS
begin
insert into table_pro_014 values (1,'王五');
end;
/

--调用存储过程
call Proc_Syntax_014('李华');

--清理环境
DROP PROCEDURE  Proc_Syntax_014;
drop table table_pro_014;