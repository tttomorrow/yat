-- @testpoint: 时间函数maketime功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入合法入参时maketime执行结果;expect:成功
insert into func_test(functionName, result) values ('maketime(''25.5'', ''30.4'', ''30'')', maketime('25.5', '30.4', '30'));
insert into func_test(functionName, result) values ('maketime(25.5, 30.4, 30)', maketime(25.5, 30.4, 30));
insert into func_test(functionName, result) values ('maketime(false, true, true)', maketime(false, true, true));
insert into func_test(functionName, result) values ('maketime(B''111'', B''111'', B''111'')', maketime(B'111', B'111', B'111'));
insert into func_test(functionName, result) values ('maketime(null, 0, 0)', maketime(null, 0, 0));
insert into func_test(functionName, result) values ('maketime(0, null, 0)', maketime(0, null, 0));
insert into func_test(functionName, result) values ('maketime(0, 0, null)', maketime(0, 0, null));
insert into func_test(functionName, result) values ('maketime(0, -1, 0)', maketime(0, -1, 0));
insert into func_test(functionName, result) values ('maketime(0, 60, 0)', maketime(0, 60, 0));
insert into func_test(functionName, result) values ('maketime(0, 60, 0)', maketime(0, 59.5, 0));
insert into func_test(functionName, result) values ('maketime(0, 0, -1)', maketime(0, 0, -1));
insert into func_test(functionName, result) values ('maketime(0, 0, 60)', maketime(0, 0, 60));
insert into func_test(functionName, result) values ('maketime(0, 0, pow(10,18))', maketime(0, 0, pow(10,18)));
insert into func_test(functionName, result) values ('maketime(0, 0, 59.9999)', maketime(0, 0, 59.9999));
insert into func_test(functionName, result) values ('maketime(0, 0, 59.999999001)', maketime(0, 0, 59.999999001));
insert into func_test(functionName, result) values ('maketime(838, 59, 58.999999)', maketime(838, 59, 58.999999));
insert into func_test(functionName, result) values ('maketime(-838, 59, 58.999999)', maketime(-838, 59, 58.999999));
insert into func_test(functionName, result) values ('maketime(25, 30, 30)', maketime(25, 30, 30));
insert into func_test(functionName, result) values ('maketime(-25, 30, 30)', maketime(-25, 30, 30));
insert into func_test(functionName, result) values ('maketime(pow(2, 32),0,0)', maketime(pow(2, 32),0,0));
insert into func_test(functionName, result) values ('maketime(-pow(2, 32),0,0)', maketime(-pow(2, 32),0,0));
insert into func_test(functionName, result) values ('maketime(0, 59, 59.9999994999)', maketime(0, 59, 59.9999994999));
insert into func_test(functionName, result) values ('maketime(0, 10, 59.999999500)', maketime(0, 10, 59.999999500));
insert into func_test(functionName, result) values ('maketime(0, 59, 59.999999500)', maketime(0, 59, 59.999999500));
insert into func_test(functionName, result) values ('maketime(0, 59, 59.999998500)', maketime(0, 59, 59.999998500));
insert into func_test(functionName, result) values ('maketime(839, 0, 0)', maketime(839, 0, 0));
insert into func_test(functionName, result) values ('maketime(-839, 0, 0)', maketime(-839, 0, 0));
insert into func_test(functionName, result) values ('maketime(838, 59, 59.000001)', maketime(838, 59, 59.000001));
insert into func_test(functionName, result) values ('maketime(838, 59, 59.000000600)', maketime(838, 59, 59.000000600));

--step3:插入非法入参时maketime执行结果;expect:合理报错
insert into func_test(functionName, result) values ('maketime(''ABCD'', 0, 0)', maketime('ABCD', 0, 0));
insert into func_test(functionName, result) values ('maketime(''a'', 0, 0)', maketime('a', 0, 0));
insert into func_test(functionName, result) values ('maketime(0, ''abcd'', 0)', maketime(0, 'abcd', 0));
insert into func_test(functionName, result) values ('maketime(0, ''a'', 0)', maketime(0, 'a', 0));

--step4:查看maketime函数执行结果是否正确;expect:成功
select * from func_test;

--step5:清理环境;expect:成功
drop table if exists func_test;