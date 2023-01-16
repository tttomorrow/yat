-- @date: 2023-01-01
-- @testpoint: 描述本用例的测试项，部分测试点合理报错。

--step1:创建普通行存表，engine参数值为非字符串;expect:报错ERROR:  syntax error
drop table if exists b_b_grammar_0001_01;
create table b_b_grammar_0001_01(a text(10),b tinytext,c mediumtext,d longtext) engine =123*$&*;

--step2:engine参数值为空;expect:成功
drop table if exists b_b_grammar_0001_02;
create table b_b_grammar_0001_02(a text(10),b tinytext,c mediumtext,d longtext) engine ='';

--step3:插入数据;expect:成功
insert into b_b_grammar_0001_02 values('测试*(%','数据库','mysql','插件');

--step4:删表;expect:成功
drop table b_b_grammar_0001_02;

