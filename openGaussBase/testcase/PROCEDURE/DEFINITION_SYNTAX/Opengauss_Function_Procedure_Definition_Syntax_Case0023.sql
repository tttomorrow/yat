-- @testpoint: 存储过程声明语法带 定义变量  %TYPE属性

--前置条件
drop table if exists table_pro_023;
create table table_pro_023(
id int,
name varchar2(20)
);
insert into table_pro_023 values (1,'李明'),(2,'李华'),(3,'张三');

--创建存储过程
CREATE OR REPLACE PROCEDURE Proc_Syntax_023()
IS
DECLARE
V1 table_pro_023.id%TYPE;
V2 table_pro_023.name%TYPE;
begin
select id,name into V1,V2 from table_pro_023 where id=3;
raise info 'V1=:%',V1;
raise info 'V2=:%',V2;
end;
/

--调用存储过程
call Proc_Syntax_023();

--清理环境
DROP PROCEDURE Proc_Syntax_023;
drop table if exists table_pro_023;


