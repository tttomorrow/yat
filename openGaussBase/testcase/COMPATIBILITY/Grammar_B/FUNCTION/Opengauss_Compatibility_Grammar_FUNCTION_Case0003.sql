-- @testpoint: 时间函数period_add功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入合法入参时period_add执行结果;expect:成功
insert into func_test(functionName, result) values ('period_add(''202101'', ''10'')', period_add('202101', '10'));
insert into func_test(functionName, result) values ('period_add(''202101.4'', ''10.5'')', period_add('202101.4', '10.5'));
insert into func_test(functionName, result) values ('period_add(202101.4, 10.5)', period_add(202101.4, 10.5));
insert into func_test(functionName, result) values ('period_add(true, false)', period_add(true, false));
insert into func_test(functionName, result) values ('period_add(B''1111'', B''11'')', period_add(B'1111', B'11'));
insert into func_test(functionName, result) values ('period_add(NULL, 1)', period_add(NULL, 1));
insert into func_test(functionName, result) values ('period_add(202205, NULL)', period_add(202205, NULL));
insert into func_test(functionName, result) values ('period_add(0, 1)', period_add(0, 1));
insert into func_test(functionName, result) values ('period_add(200000, 0)', period_add(200000, 0));
insert into func_test(functionName, result) values ('period_add(-202205, 1)', period_add(-202205, 1));
insert into func_test(functionName, result) values ('period_add(202205, pow(2,31))', period_add(202205, pow(2,31)));
insert into func_test(functionName, result) values ('period_add(202211, 100)', period_add(202211, 100));
insert into func_test(functionName, result) values ('period_add(197005, 7)', period_add(197005, 7));
insert into func_test(functionName, result) values ('period_add(202205, -12)', period_add(202205, -12));
insert into func_test(functionName, result) values ('period_add(1,12)', period_add(1,12));
insert into func_test(functionName, result) values ('period_add(6901,12)', period_add(6901,12));
insert into func_test(functionName, result) values ('period_add(7001,12)', period_add(7001,12));
insert into func_test(functionName, result) values ('period_add(10001,12)', period_add(10001,12));
insert into func_test(functionName, result) values ('period_add(10001, -12)', period_add(10001, -12));
insert into func_test(functionName, result) values ('period_add(10001, -12*30-1)', period_add(10001, -361));
insert into func_test(functionName, result) values ('period_add(pow(2,60), 20)', period_add(pow(2,60), 20));

--step3:插入非法入参时maketime执行结果;expect:合理报错
insert into func_test(functionName, result) values ('period_add(''abcd'', 1)', period_add('abcd', 1));
insert into func_test(functionName, result) values ('period_add(''a'', 1)', period_add('a', 1));
insert into func_test(functionName, result) values ('period_add(200000, ''abcd'')', period_add(200000, 'abcd'));
insert into func_test(functionName, result) values ('period_add(200000, ''a'')', period_add(200000, 'a'));

--step4:查看makedate函数执行结果是否正确;expect:成功
select * from func_test;

--step5:清理环境;expect:成功
drop table if exists func_test;