-- @testpoint: 存储过程声明语法带IN模式的存储过程

--创建表并插入数据
drop table if exists table_pro_003;
create table table_pro_003(id int,name varchar2(20));
insert into table_pro_003 values (1,'李明'),(2,'李华'),(3,'张三');

--创建存储过程
DROP PROCEDURE if exists Proc_Syntax_003;
CREATE OR REPLACE PROCEDURE Proc_Syntax_003(IN name1 varchar2(20))  IS
begin
insert into table_pro_003 values (1,'王五');
end;
/

--调用存储过程
CALL Proc_Syntax_003('李华');
SELECT * FROM table_pro_003;

--清理环境
DROP PROCEDURE Proc_Syntax_003;
DROP TABLE table_pro_003;