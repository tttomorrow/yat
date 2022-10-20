-- @testpoint: 时间函数time功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入time(time参数格式)且入参合法的用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIME(''00:00:00'')',TIME('00:00:00'));
insert into func_test(functionName, result) values('TIME(''240000'')',TIME('240000'));
insert into func_test(functionName, result) values('TIME(240000)',TIME(240000));
insert into func_test(functionName, result) values('TIME(240000.000001)',TIME(240000.000001));
insert into func_test(functionName, result) values('TIME(''25:30:30'')',TIME('25:30:30'));
insert into func_test(functionName, result) values('TIME(''-25:30:30'')',TIME('-25:30:30'));
insert into func_test(functionName, result) values('TIME(''838:59:59'')',TIME('838:59:59'));
insert into func_test(functionName, result) values('TIME(''-838:59:59'')',TIME('-838:59:59'));
insert into func_test(functionName, result) values('TIME(''838:0:0'')',TIME('838:0:0'));
insert into func_test(functionName, result) values('TIME(''00:00:59.9999'')',TIME('00:00:59.9999'));
insert into func_test(functionName, result) values('TIME(''00:00:59.999999000'')',TIME('00:00:59.999999000'));
insert into func_test(functionName, result) values('TIME(''83:59:59.0000000009'')',TIME('83:59:59.0000000009'));
insert into func_test(functionName, result) values('TIME(''00:10:59.999999999'')',TIME('00:10:59.999999999'));
insert into func_test(functionName, result) values('TIME(''00:59:59.999999999'')',TIME('00:59:59.999999999'));
insert into func_test(functionName, result) values('TIME(''83:59:59.0000000004'')',TIME('83:59:59.0000000004'));
insert into func_test(functionName, result) values('TIME(''0:0:-1'')',TIME('0:0:-1'));
insert into func_test(functionName, result) values('TIME(''0:-1:0'')',TIME('0:-1:0'));
insert into func_test(functionName, result) values('TIME(''838:59:59.000000500'')',TIME('838:59:59.000000500'));

--step3:插入time(time参数格式)但涉及时间类型值超出范围的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIME(''839:0:0'')',TIME('839:0:0'));
insert into func_test(functionName, result) values('TIME(''-839:0:0'')',TIME('-839:0:0'));

--step4:插入time(datetime参数格式)且入参合法的用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIME(''2003-12-31 01:02:03'')', TIME('2003-12-31 01:02:03'));
insert into func_test(functionName, result) values('TIME(''20031231010203'')', TIME('20031231010203'));
insert into func_test(functionName, result) values('TIME(''2003-12-31 01:02:03.000123'')', TIME('2003-12-31 01:02:03.000123'));
insert into func_test(functionName, result) values('TIME(''20031231010203.000123'')', TIME('20031231010203.000123'));
insert into func_test(functionName, result) values('TIME(20031231010203)', TIME(20031231010203));
insert into func_test(functionName, result) values('TIME(20031231010203.000123)', TIME(20031231010203.000123));
insert into func_test(functionName, result) values('TIME(''2003-12-31 01:02:03.0001234'')',TIME('2003-12-31 01:02:03.0001234'));
insert into func_test(functionName, result) values('TIME(''2003-12-31 01:02:03.0001235'')', TIME('2003-12-31 01:02:03.0001235'));
insert into func_test(functionName, result) values('TIME(''2003-12-31 01:02:03.00012345'')', TIME('2003-12-31 01:02:03.00012345'));
insert into func_test(functionName, result) values('TIME(''20031231010203.0001235'')', TIME('20031231010203.0001235'));

--step5:插入time(datetime参数格式)但涉及时间类型值超出范围的的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIME(''10000-01-01 00:00:00'')', TIME('10000-01-01 00:00:00'));
insert into func_test(functionName, result) values('TIME(''0000-12-31 59:59:59'')', TIME('0000-12-31 59:59:59'));

--step6:插入入参为特殊类型的time用例执行结果;expect:成功
insert into func_test(functionName, result) values('TIME(time''1:1:1'')', TIME(time'1:1:1'));
insert into func_test(functionName, result) values('TIME(date''2000-01-01'')', TIME(date'2000-01-01'));
insert into func_test(functionName, result) values('TIME(cast(''2001-12-10 23:59:59'' as datetime))', TIME(cast('2001-12-10 23:59:59' as datetime)));
insert into func_test(functionName, result) values('TIME(false)', TIME(false));
insert into func_test(functionName, result) values('TIME(B''1'')', TIME(B'1'));

--step7:插入非法入参时time执行结果;expect:合理报错
insert into func_test(functionName, result) values('TIME(''0:60:0'')',TIME('0:60:0'));
insert into func_test(functionName, result) values('TIME(''0:59.5:0'')',TIME('0:59.5:0'));
insert into func_test(functionName, result) values('TIME(''0:59.4:0'')',TIME('0:59.4:0'));
insert into func_test(functionName, result) values('TIME(''0:0:60'')',TIME('0:0:60'));
insert into func_test(functionName, result) values('TIME(''2003-12-40 01:02:03'')', TIME('2003-12-40 01:02:03'));
insert into func_test(functionName, result) values('TIME(''2003-13-31 01:02:03.000123'')', TIME('2003-13-31 01:02:03'));
insert into func_test(functionName, result) values('TIME(''9999-12-31 59:59:59'')', TIME('9999-12-31 59:59:59'));

--step8:查看time函数执行结果是否正确;expect:成功
select * from func_test;

--step9:清理环境;expect:成功
drop table if exists func_test;