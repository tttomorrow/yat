--  @testpoint:使用explain语法，对参数中的取值进行无效值测试，合理报错
--建表
drop table if exists student;
create table student(id int, name char(20));
--analyze参数取值为null,合理报错
explain (analyze null) insert into student values(5,'a'),(6,'b');
--analyze参数取值为10，合理报错
explain (analyze 10) insert into student values(5,'a'),(6,'b');
--plan参数取值为open，合理报错
explain (plan open) insert into student values(5,'a'),(6,'b');
--plan参数取值为null，合理报错
explain (plan null) insert into student values(5,'a'),(6,'b');
--删除表
drop table student;