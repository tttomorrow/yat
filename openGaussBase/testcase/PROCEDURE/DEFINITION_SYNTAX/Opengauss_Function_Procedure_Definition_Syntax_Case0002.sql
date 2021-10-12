-- @testpoint: 存储过程声明语法空参的存储过程 创建存储过程时使用IS

DROP PROCEDURE if exists Proc_Syntax_002;

CREATE OR REPLACE PROCEDURE Proc_Syntax_002()  IS
begin
    drop table if exists table_pro_002;
    create table table_pro_002 (id int,name varchar2(20));
    INSERT INTO table_pro_002 values (1,'hauwei');
end;
/

--调用存储过程
CALL Proc_Syntax_002();

--清理环境
DROP PROCEDURE Proc_Syntax_002;
DROP TABLE table_pro_002;