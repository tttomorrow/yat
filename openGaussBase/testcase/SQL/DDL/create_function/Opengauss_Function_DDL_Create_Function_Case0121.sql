--  @testpoint:创建函数，指定函数的语言的名称是SQL,函数体内使用insert语句
   drop table if EXISTS emp cascade;
   CREATE TABLE emp (
        name        text,
        salary      numeric,
        age         integer
    );
drop function if exists double_salary();
 CREATE FUNCTION double_salary() RETURNS void  AS $$
       insert into emp values('lily',8504.5,25);
    $$ LANGUAGE SQL;
    /
 select * from emp;
 drop table emp;
 drop FUNCTION double_salary;