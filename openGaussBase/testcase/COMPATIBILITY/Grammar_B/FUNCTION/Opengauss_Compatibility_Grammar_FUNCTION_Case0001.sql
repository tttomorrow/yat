-- @testpoint: 时间函数makedate功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入合法入参时makedate执行结果;expect:成功
insert into func_test(functionName, result) values ('makedate(''2003'',''61'')', makedate('2003','61'));
insert into func_test(functionName, result) values ('makedate(''12.4'',''12.5'')', makedate('12.4','12.5'));
insert into func_test(functionName, result) values ('makedate(12.4,12.5)', makedate(12.4,12.5));
insert into func_test(functionName, result) values ('makedate(false, true)', makedate(false, true));
insert into func_test(functionName, result) values ('makedate(B''101'', B''101'')', makedate(B'101', B'101'));
insert into func_test(functionName, result) values ('makedate(null, 10)', makedate(null, 10));
insert into func_test(functionName, result) values ('makedate(2000, null)', makedate(2000, null));
insert into func_test(functionName, result) values ('makedate(-1, 20)', makedate(-1, 20));
insert into func_test(functionName, result) values ('makedate(10000, 20)', makedate(10000, 20));
insert into func_test(functionName, result) values ('makedate(2000, 0)', makedate(2000, 0));
insert into func_test(functionName, result) values ('makedate(2000, 60)', makedate(2000, 60));
insert into func_test(functionName, result) values ('makedate(2000, 380)', makedate(2000, 380));
insert into func_test(functionName, result) values ('makedate(69, 32)',makedate(69, 32));
insert into func_test(functionName, result) values ('makedate(70, 32)', makedate(70, 32));
insert into func_test(functionName, result) values ('makedate(100,32)', makedate(100,32));
insert into func_test(functionName, result) values ('makedate(9999,366)', makedate(9999,366));
insert into func_test(functionName, result) values ('makedate(pow(2,62),366)', makedate(pow(2,62),366));

--step3:插入非法入参时makedate执行结果;expect:合理报错
insert into func_test(functionName, result) values ('makedate(''abcd'', ''61'')', makedate('abcd', '61'));

--step4:查看makedate函数执行结果是否正确;expect:成功
select * from func_test;

--step5:清理环境;expect:成功
drop table if exists func_test;