-- @testpoint: 存储过程声明语法空参的存储过程 创建存储过程时使用AS

DROP PROCEDURE if exists Proc_Syntax_001;
CREATE OR REPLACE PROCEDURE Proc_Syntax_001() AS
begin
    drop table if exists table_pro_001;
    create table table_pro_001 (id int,name varchar2(20));
    INSERT INTO table_pro_001 values (1,'hauwei');
end;
/

--调用存储过程
CALL Proc_Syntax_001();

--清理环境
DROP PROCEDURE Proc_Syntax_001;
DROP TABLE table_pro_001;















-- 创建存储过程

create or replace procedure FVT_PROC_CLOB_001() is
V1 CLOB;
begin
  IF V1 is NULL then
  raise info 'V1 is NULL';
  else
  raise info 'V1 is not NULL';
  end if;
end;
/
--调用存储过程
CALL FVT_PROC_CLOB_001();

--恢复环境
DROP procedure if exists FVT_PROC_CLOB_001;



