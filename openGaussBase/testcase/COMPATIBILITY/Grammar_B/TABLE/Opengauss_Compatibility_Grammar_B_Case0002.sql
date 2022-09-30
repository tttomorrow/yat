-- @testpoint: engine参数取值测试，部分测试点合理报错
--step1:创建普通行存表，engine参数值为非字符串;expect:报错ERROR:  syntax error
drop table if exists tb_b_grammar_0002_01;
create table tb_b_grammar_0002_01(a text(10),b tinytext,c mediumtext,d longtext) engine =123*$&*;

--step2:engine参数值为空;expect:成功
drop table if exists tb_b_grammar_0002_02;
create table tb_b_grammar_0002_02(a text(10),b tinytext,c mediumtext,d longtext) engine ='';

--step3:省略=;expect:成功
drop table if exists tb_b_grammar_0002_03;
create table tb_b_grammar_0002_03(a text(10),b tinytext,c mediumtext,d longtext) engine 引擎;

--step4:插入数据;expect:成功
insert into tb_b_grammar_0002_03 values('测试*(%','数据库','mysql','插件');

--step5:engine参数错误;expect:合理报错ERROR:  syntax error
drop table if exists tb_b_grammar_0002_04;
create table tb_b_grammar_0002_04(a text(10),b tinytext,c mediumtext,d longtext) engines 引擎;

--step6:engine参数值为数字开头;expect:合理报错ERROR:  syntax error at
drop table if exists tb_b_grammar_0002_05;
create table tb_b_grammar_0002_05(a text(10),b tinytext,c mediumtext,d longtext) engines 1_er;

--step7:删表;expect:成功
drop table tb_b_grammar_0002_03;


