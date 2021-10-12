-- @testpoint: 存储过程声明语法带OUT模式的存储过程

--前置条件
drop table if exists stu_004;
create table stu_004(
id int,
sname varchar2(20),
sage number(2),
ssex varchar2(5)
);
insert into stu_004 values (1,'张三',23,'男');
insert into stu_004 values (2,'李四',23,'男');
insert into stu_004 values (3,'吴鹏',25,'男');
insert into stu_004 values (4,'琴沁',20,'女');
insert into stu_004 values (5,'王丽',20,'女');
insert into stu_004 values (6,'李波',21,'男');
insert into stu_004 values (7,'刘玉',21,'男');
insert into stu_004 values (8,'萧蓉',21,'女');
insert into stu_004 values (9,'陈萧晓',23,'女');
insert into stu_004 values (10,'陈美',22,'女');

--创建存储过程
DROP PROCEDURE if exists Proc_Syntax_004;
CREATE OR REPLACE PROCEDURE Proc_Syntax_004(num out int)  IS
begin
select id into num from stu_004 where sage=25;
raise info ':%',num;
end;
/

--调用存储过程
call Proc_Syntax_004(1);

--清理环境
DROP PROCEDURE Proc_Syntax_004;
DROP TABLE stu_004;