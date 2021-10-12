-- @testpoint: 存储过程声明语法带 定义变量  %ROWTYPE属性

--前置条件
drop table if exists table_pro_023;
create table table_pro_023(
id int,
name varchar2(20)
);
insert into table_pro_023 values (1,'李明'),(2,'李华'),(3,'张三');

drop table if exists table_pro_024;
create table table_pro_024(
id int,
name varchar2(20)
);
insert into table_pro_024 values (1,'李明'),(2,'李华'),(3,'张三');

--创建存储过程
CREATE OR REPLACE PROCEDURE Proc_Syntax_024()
AS
V1 table_pro_023%ROWTYPE;
begin
select * into V1 from table_pro_024 where id=2;
raise info 'V1=:%',V1.id;
raise info 'V1=:%',V1.name;
end;
/

--调用存储过程
call Proc_Syntax_024();

--清理环境
DROP PROCEDURE Proc_Syntax_024;
drop table if exists table_pro_023;
drop table if exists table_pro_024;


