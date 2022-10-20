-- @testpoint: 时间函数period_diff功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入合法入参时period_diff执行结果;expect:成功
insert into func_test(functionName, result) values ('period_diff(''202101'', ''202102'')', period_diff('202101', '202102'));
insert into func_test(functionName, result) values ('period_diff(''202101.4'', ''202102.5'')', period_diff('202101.4', '202102.5'));
insert into func_test(functionName, result) values ('period_diff(202101.4, 202102.5)', period_diff(202101.4, 202102.5));
insert into func_test(functionName, result) values ('period_diff(true, false)', period_diff(true, false));
insert into func_test(functionName, result) values ('period_diff(B''1111'', B''11111''))', period_diff(B'1111', B'11111'));
insert into func_test(functionName, result) values ('period_diff(NULL, 200001)', period_diff(NULL, 200001));
insert into func_test(functionName, result) values ('period_diff(202011, NULL)', period_diff(202011, NULL));
insert into func_test(functionName, result) values ('period_diff(-202011, 200001)', period_diff(-202011, 200001));
insert into func_test(functionName, result) values ('period_diff(202011, -200001)', period_diff(202011, -200001));
insert into func_test(functionName, result) values ('period_diff(707712, 202201)', period_diff(707712, 202201));
insert into func_test(functionName, result) values ('period_diff(6912, 10001)', period_diff(6912, 10001));
insert into func_test(functionName, result) values ('period_diff(7001, 10001)', period_diff(7001, 10001));
insert into func_test(functionName, result) values ('period_diff(10002, 6901)', period_diff(10002, 6901));
insert into func_test(functionName, result) values ('period_diff(10002, 7001)', period_diff(10002, 7001));
insert into func_test(functionName, result) values ('period_diff(0, 30)', period_diff(0, 30));
insert into func_test(functionName, result) values ('period_diff(30, 0)', period_diff(30, 0));
insert into func_test(functionName, result) values ('period_diff(pow(2,62), pow(2,60))', period_diff(pow(2,62), pow(2,60)));

--step3:插入非法入参时period_diff执行结果;expect:合理报错
insert into func_test(functionName, result) values ('period_diff(''abcd'', 200001)', period_diff('abcd', 200001));
insert into func_test(functionName, result) values ('period_diff(''a'', 200001)', period_diff('a', 200001));
insert into func_test(functionName, result) values ('period_diff(200001, ''abcd'')', period_diff(200001, 'abcd'));
insert into func_test(functionName, result) values ('period_diff(200001, ''a'')', period_diff(200001, 'a'));

--step4:查看makedate函数执行结果是否正确;expect:成功
select * from func_test;

--step5:清理环境;expect:成功
drop table if exists func_test;