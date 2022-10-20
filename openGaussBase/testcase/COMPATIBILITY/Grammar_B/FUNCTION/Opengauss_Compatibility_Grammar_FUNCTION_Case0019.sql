-- @testpoint: 时间函数UTC_TIME功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入UTC_TIME正常执行结果;expect:成功
insert into func_test(functionName, result) values('UTC_TIME', UTC_TIME);
insert into func_test(functionName, result) values('UTC_TIME()', UTC_TIME());
insert into func_test(functionName, result) values('UTC_TIME(0)', UTC_TIME(0));
insert into func_test(functionName, result) values('UTC_TIME(1)', UTC_TIME(1));
insert into func_test(functionName, result) values('UTC_TIME(2)', UTC_TIME(2));
insert into func_test(functionName, result) values('UTC_TIME(3)', UTC_TIME(3));
insert into func_test(functionName, result) values('UTC_TIME(4)', UTC_TIME(4));
insert into func_test(functionName, result) values('UTC_TIME(5)', UTC_TIME(5));
insert into func_test(functionName, result) values('UTC_TIME(6)', UTC_TIME(6));

--step3:插入非法入参下UTC_TIME执行结果;expect:合理报错
insert into func_test(functionName, result) values('UTC_TIME(-1)', UTC_TIME(-1));

--step4:查看UTC_TIME函数执行结果是否正确;expect:成功
select * from func_test;

--step5:清理环境;expect:成功
drop table if exists func_test;