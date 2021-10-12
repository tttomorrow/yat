-- @testpoint: 存储过程声明语法带 DECLARE声明 隐式游标定义 SQL%FOUND布尔型属性

drop table if exists stu;
create table stu(
sno int primary key,
sname varchar2(20),
sage number(2),
ssex varchar2(5)
);

drop table if exists course;
create table course(
cno int,
cname varchar2(20),
tno varchar2(20),
ssex varchar2(5)
);

insert into stu values (001,'张三',23,'男');
insert into stu values (002,'李四',23,'男');
insert into stu values (003,'吴鹏',25,'男');
insert into stu values (004,'琴沁',20,'女');
insert into stu values (005,'王丽',20,'女');
insert into stu values (006,'李波',21,'男');
insert into stu values (007,'刘玉',21,'男');
insert into stu values (008,'萧蓉',21,'女');
insert into stu values (009,'陈萧晓',23,'女');
insert into stu values (010,'陈美',22,'女');


insert into course values (001,'J2SE','t002');
insert into course values (002,'Java Web','t002');
insert into course values (003,'SSH','t001');
insert into course values (004,'Oracle','t001');
insert into course values (005,'SQL SERVER 2005','t003');
insert into course values (006,'C#','t003');
insert into course values (007,'JavaScript','t002');
insert into course values (008,'DIV+CSS','t001');
insert into course values (009,'PHP','t003');
insert into course values (010,'EJB3.0','t002');

--创建存储过程
CREATE OR REPLACE PROCEDURE Proc_Syntax_027()
AS
    DECLARE
    V_DEPTNO int := 005;
    BEGIN
        DELETE FROM stu WHERE sno = V_DEPTNO;
        IF SQL%FOUND THEN
        DELETE FROM course WHERE cno = V_DEPTNO;
        END IF;
    END;
/

--调用存储过程
CALL Proc_Syntax_027();

--清理环境
drop procedure Proc_Syntax_027;
drop table stu;
drop table course;
