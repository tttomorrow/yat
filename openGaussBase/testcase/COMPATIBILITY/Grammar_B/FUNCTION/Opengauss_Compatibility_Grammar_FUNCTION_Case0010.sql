-- @testpoint: 时间函数time_format功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入合法入参下时分秒毫秒相关format格式的用例执行结果;expect:成功
insert into func_test(functionName, result) values(' TIME_FORMAT(''00:00:00'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('00:00:00', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''240000'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('240000', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(240000, ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT(240000, '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(240000.000001, ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT(240000.000001, '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''25:30:30'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('25:30:30', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''-25:30:30'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('-25:30:30', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''838:59:59'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('838:59:59', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''-838:59:59'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('-838:59:59', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''838:0:0'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('838:0:0', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''00:00:59.9999'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('00:00:59.9999', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''00:00:59.999999000'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('00:00:59.999999000', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''83:59:59.0000000009'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('83:59:59.0000000009', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''00:10:59.999999999'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('00:10:59.999999999', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''00:59:59.999999999'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('00:59:59.999999999', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''838:59:59.000000500'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('838:59:59.000000500', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''83:59:59.0000000004'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('83:59:59.0000000004', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''0:-1:0'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('0:-1:0', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''0:0:-1'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('0:0:-1', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));

insert into func_test(functionName, result) values(' TIME_FORMAT(''2003-12-31 01:02:03.0123'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('2003-12-31 01:02:03.0123', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''20031231010203.0123'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('20031231010203.0123', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(20031231010203, ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT(20031231010203, '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(20031231010203.0123, ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT(20031231010203.0123, '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''0000-12-31 23:59:59'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('0000-12-31 23:59:59', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));

--step3:插入time_format涉及时间类型值超出范围的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values(' TIME_FORMAT(''839:0:0'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('839:0:0', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''-839:0:0'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('-839:0:0', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''10000-01-01 01:01:01'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('10000-01-01 01:01:01', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));

--step4:插入入参为特殊类型的time_format用例执行结果;expect:成功
insert into func_test(functionName, result) values(' TIME_FORMAT(date''2021-12-31'', ''%T|%r||%f'')    ', TIME_FORMAT(date'2021-12-31', '%T|%r||%f'));
insert into func_test(functionName, result) values(' TIME_FORMAT(time''01:01:01'', ''%T|%r||%f'')    ', TIME_FORMAT(time'01:01:01', '%T|%r||%f'));
insert into func_test(functionName, result) values(' TIME_FORMAT(cast(''2001-12-10 23:59:59'' as datetime), ''%T|%r||%f'')    ', TIME_FORMAT(cast('2001-12-10 23:59:59' as datetime), '%T|%r||%f'));
insert into func_test(functionName, result) values(' TIME_FORMAT(B''1'', ''%T|%r||%f'')    ', TIME_FORMAT(B'1', '%T|%r||%f'));
insert into func_test(functionName, result) values(' TIME_FORMAT(false, ''%T|%r||%f'')    ', TIME_FORMAT(false, '%T|%r||%f'));

--step5:插入非法入参时time_format执行结果;expect:合理报错
insert into func_test(functionName, result) values(' TIME_FORMAT(''0:60:0'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('0:60:0', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''0:59.5:0'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('0:59.5:0', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''0:59.4:0'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('0:59.4:0', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''0:0:60'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('0:0:60', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''2021-12-31'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('2021-12-31', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''2021-12-32 01:01:01'', ''%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'')    ', TIME_FORMAT('2021-12-32 01:01:01', '%T|%r|%H|%h|%I|%i|%S|%f|%p|%k'));

--step6:插入合法入参下非时分秒毫秒相关format格式的用例执行结果;expect:成功
insert into func_test(functionName, result) values(' TIME_FORMAT(''100:59:59.0123'', ''%a|%b|%c|%D|%d|%e|%j|%M|%m'')    ', TIME_FORMAT('100:59:59.0123', '%a|%b|%D|%j|%M|%U|%u|%V|%v|%W|%w|%X|%x'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''100:59:59.0123'', ''%U|%u|%V|%v|%W|%w|%X|%x|%Y|%y'')    ', TIME_FORMAT('100:59:59.0123', '%c|%d|%e|%m|%Y|%y'));
insert into func_test(functionName, result) values(' TIME_FORMAT(''100:59:59.0123'', ''%N|%n abcd'')    ', TIME_FORMAT('100:59:59.0123', '%N|%n abcd'));

--step7: og时间类型与格式测试;expect:部分类型合理报错
insert into func_test(functionName, result) values('time_format(timetz''1:0:0+05'', ''%T|%r|%h|%h'')', time_format(timetz'1:0:0+05', '%T|%r|%h|%h'));
insert into func_test(functionName, result) values('time_format(timestamptz''2000-1-1 1:1:1+05'', ''%T|%r|%h|%h'')', time_format(timestamptz'2000-1-1 1:1:1+05', '%T|%r|%h|%h'));
insert into func_test(functionName, result) values('time_format(reltime''2000 years 1 mons 1 days 1:1:1'', ''%T|%r|%h|%h'')', time_format(reltime'2000 years 1 mons 1 days 1:1:1', '%T|%r|%h|%h'));
insert into func_test(functionName, result) values('time_format(abstime''2000-1-1 1:1:1+05'', ''%T|%r|%h|%h'')', time_format(abstime'2000-1-1 1:1:1+05', '%T|%r|%h|%h'));
insert into func_test(functionName, result) values('time_format(''23:0:0+05'', ''%T|%r|%h|%h'')', time_format('23:0:0+05', '%T|%r|%h|%h'));
insert into func_test(functionName, result) values('time_format(''2000 years 1 mons 1 days 1:1:1'', ''%T|%r|%h|%h'')', time_format('2000 years 1 mons 1 days 1:1:1', '%T|%r|%h|%h'));
insert into func_test(functionName, result) values('time_format(''2000-1-1 23:1:1+05'', ''%T|%r|%h|%h'')', time_format('2000-1-1 23:1:1+05', '%T|%r|%h|%h'));

--step8: og时间边界测试;expect:合理报错
insert into func_test(functionName, result) values('time_format(date''4714-11-24bc'', ''%T|%r|%h|%h'')', time_format(date'4714-11-24bc', '%T|%r|%h|%h'));
insert into func_test(functionName, result) values('time_format(date''5874897-12-31'', ''%T|%r|%h|%h'')', time_format(date'5874897-12-31', '%T|%r|%h|%h'));
insert into func_test(functionName, result) values('time_format(datetime''4714-11-24 00:00:00 bc'', ''%T|%r|%h|%h'')', time_format(datetime'4714-11-24 00:00:00 bc', '%T|%r|%h|%h'));
insert into func_test(functionName, result) values('time_format(datetime''294277-1-9 4:00:54.775807'', ''%T|%r|%h|%h'')', time_format(datetime'294277-1-9 4:00:54.775807', '%T|%r|%h|%h'));
insert into func_test(functionName, result) values('time_format(datetime''294277-1-9 4:00:54.775806'', ''%T|%r|%h|%h'')', time_format(datetime'294277-1-9 4:00:54.775806', '%T|%r|%h|%h'));

--step9:查看time_format函数执行结果是否正确;expect:成功
select * from func_test;

--step10:清理环境;expect:成功
drop table if exists func_test;