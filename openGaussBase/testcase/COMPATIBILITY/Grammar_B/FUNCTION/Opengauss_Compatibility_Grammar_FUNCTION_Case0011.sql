-- @testpoint: 时间函数timestamp(单参数)功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入timestamp入参合法的用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIMESTAMP(''2003-12-31'')', TIMESTAMP('2003-12-31'));
insert into func_test(functionName, result) values('TIMESTAMP(''20031231'')', TIMESTAMP('20031231'));
insert into func_test(functionName, result) values('TIMESTAMP(20031231)', TIMESTAMP(20031231));
insert into func_test(functionName, result) values('TIMESTAMP(''2003-12-31 12:00:00.123456'')', TIMESTAMP('2003-12-31 12:00:00.123456'));
insert into func_test(functionName, result) values('TIMESTAMP(''20000229120000.1234567'')', TIMESTAMP('20000229120000.1234567'));
insert into func_test(functionName, result) values('TIMESTAMP(20000229120000.1234567)', TIMESTAMP(20000229120000.1234567));
insert into func_test(functionName, result) values('TIMESTAMP(20000229120000)', TIMESTAMP(20000229120000));
insert into func_test(functionName, result) values('TIMESTAMP(''9999-12-31'')', TIMESTAMP('9999-12-31'));
insert into func_test(functionName, result) values('TIMESTAMP(''9999-12-31 23:59:59.999999'')', TIMESTAMP('9999-12-31 23:59:59.999999'));
insert into func_test(functionName, result) values('TIMESTAMP(''0000-01-01'')', TIMESTAMP('0000-01-01'));
insert into func_test(functionName, result) values('TIMESTAMP(''0000-01-01 00:00:00.000001'')', TIMESTAMP('0000-01-01 00:00:00.000001'));

--step3:插入timestamp涉及时间类型值超出范围的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMESTAMP(''10000-01-01'')', TIMESTAMP('10000-01-01'));
insert into func_test(functionName, result) values('TIMESTAMP(''10000-01-01 00:00:00'')', TIMESTAMP('10000-01-01 00:00:00'));
--step4:插入入参为特殊类型的timestamp用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIMESTAMP(date''2003-01-01'')', TIMESTAMP(date'2003-01-01'));
insert into func_test(functionName, result) values('TIMESTAMP(cast(''2007-12-10 23:59:59'' as datetime))', TIMESTAMP(cast('2007-12-10 23:59:59' as datetime)));
insert into func_test(functionName, result) values('TIMESTAMP(null)', TIMESTAMP(null));

--step5:插入非法入参时timestamp执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIMESTAMP(''2003-13-01'')', TIMESTAMP('2003-13-01'));
insert into func_test(functionName, result) values('TIMESTAMP(''2003-2-29'')', TIMESTAMP('2003-2-29'));
insert into func_test(functionName, result) values('TIMESTAMP(''2003-12-31 25:00:00'')', TIMESTAMP('2003-12-31 25:00:00'));
insert into func_test(functionName, result) values('TIMESTAMP(''2003-12-31 23:60:00'')', TIMESTAMP('2003-12-31 23:60:00'));
insert into func_test(functionName, result) values('TIMESTAMP(''2003-12-31 23:59:60'')', TIMESTAMP('2003-12-31 23:59:60'));
insert into func_test(functionName, result) values('TIMESTAMP(''asdasd'')', TIMESTAMP('asdasd'));
insert into func_test(functionName, result) values('TIMESTAMP(true)', TIMESTAMP(true));
insert into func_test(functionName, result) values('TIMESTAMP(B''1'')', TIMESTAMP(B'1'));

--step6: og时间类型与格式测试;expect:部分类型合理报错
insert into func_test(functionName, result) values('timestamp(timetz''1:1:1+05'')', timestamp(timetz'1:1:1+05'));
insert into func_test(functionName, result) values('timestamp(timestamptz''2000-1-1 1:1:1+05'')', timestamp(timestamptz'2000-1-1 1:1:1+05'));
insert into func_test(functionName, result) values('timestamp(reltime''2000 years 1 mons 1 days 1:1:1'')', timestamp(reltime'2000 years 1 mons 1 days 1:1:1'));
insert into func_test(functionName, result) values('timestamp(abstime''2000-1-1 1:1:1+05'')', timestamp(abstime'2000-1-1 1:1:1+05'));
insert into func_test(functionName, result) values('timestamp(''23:1:1+05'')', timestamp('23:1:1+05'));
insert into func_test(functionName, result) values('timestamp(''2000 years 1 mons 1 days 1:1:1'')', timestamp('2000 years 1 mons 1 days 1:1:1'));
insert into func_test(functionName, result) values('timestamp(''2000-1-1 23:1:1+05'')', timestamp('2000-1-1 23:1:1+05'));

--step7: og时间边界测试;expect:合理报错
insert into func_test(functionName, result) values('timestamp(date''4714-11-24bc'')', timestamp(date'4714-11-24bc'));
insert into func_test(functionName, result) values('timestamp(date''5874897-12-31'')', timestamp(date'5874897-12-31'));
insert into func_test(functionName, result) values('timestamp(datetime''4714-11-24 00:00:00 bc'')', timestamp(datetime'4714-11-24 00:00:00 bc'));
insert into func_test(functionName, result) values('timestamp(datetime''294277-1-9 4:00:54.775807'')', timestamp(datetime'294277-1-9 4:00:54.775807'));
insert into func_test(functionName, result) values('timestamp(datetime''294277-1-9 4:00:54.775806'')', timestamp(datetime'294277-1-9 4:00:54.775806'));

--step8:查看timestamp函数执行结果是否正确;expect:成功
select * from func_test;

--step9:清理环境;expect:成功
drop table if exists func_test;