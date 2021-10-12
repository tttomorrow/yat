-- @testpoint: 存储过程内变量区分大小写
drop table if exists stu;
create table stu(
sno int primary key,
sname varchar2(20),
sage number(2),
ssex varchar2(5)
);

insert into stu values (005,'王丽',20,'女');

create or replace procedure Proc_Syntax_036()
is
v_sname varchar2(20);
begin
  select sname,sage into V_SNAME from stu where sno=005;
  raise info '查询符合条件的学生姓名和年龄：%',v_sname;
  end;
  /

--清理环境
call Proc_Syntax_036();
DROP procedure Proc_Syntax_036;
drop table if exists stu;
