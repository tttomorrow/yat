-- @testpoint: 时间函数subtime功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入subtime(datetime, time)参数格式且入参合法的用例执行结果;expect:成功
insert into func_test(functionName, result) values('subtime(''2000-02-28 20:59:59'', ''-25:00'')', subtime('2000-02-28 20:59:59', '-25:00') );
insert into func_test(functionName, result) values('subtime(''2000-02-28 20:59:59'', ''25:00'')', subtime('2000-02-28 20:59:59', '25:00') );
insert into func_test(functionName, result) values('subtime(''2007-12-31 23:59:59.999999'',''1 1:1:1.000002'')', subtime('2007-12-31 23:59:59.999999','1 1:1:1.000002'));
insert into func_test(functionName, result) values('subtime(''2007-12-31 0:0:0.999999'',''1 1:1:1.000002'')', subtime('2007-12-31 0:0:0.999999','1 1:1:1.000002'));
insert into func_test(functionName, result) values('subtime(''2007-12-31 23:59:59.999999'',''1 1:1:1.000002'')', subtime('2007-12-31 23:59:59.999999','1 1:1:1.000002'));
insert into func_test(functionName, result) values('subtime(''20000228205959'', ''250000'')', subtime('20000228205959', '250000') );
insert into func_test(functionName, result) values('subtime(''20000228205959.000002'', ''250000.000001'')', subtime('20000228205959.000002', '250000.000001') );
insert into func_test(functionName, result) values('subtime(20000228205959, 250000)', subtime(20000228205959, 250000) );
insert into func_test(functionName, result) values('subtime(20000228205959.000002, 250000.000001)', subtime(20000228205959.000002, 250000.000001) );
insert into func_test(functionName, result) values('subtime(''2000-02-28 20:59:59'', NULL)', subtime('2000-02-28 20:59:59', NULL) );
insert into func_test(functionName, result) values('subtime(NULL, ''-25:00'')', subtime(NULL, '-25:00') );
insert into func_test(functionName, result) values('subtime(''0001-01-1 20:59:59'', ''21:00'');', subtime('0001-01-1 20:59:59', '21:00')   );

--step3:插入subtime(datetime, time)参数格式但涉及时间类型值超出范围的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('subtime(''2007-12-31 23:59:59.999999'',''100 1:1:1.000002'')',subtime('2007-12-31 23:59:59.999999','100 1:1:1.000002'));
insert into func_test(functionName, result) values('subtime(''9999-12-31 20:59:59'', ''-3:00:1'')', subtime('9999-12-31 20:59:59', '-3:00:1') );
insert into func_test(functionName, result) values('subtime(''10000-1-1 20:59:59'', ''30:00:1'')', subtime('10000-1-1 20:59:59', '30:00:1') );
insert into func_test(functionName, result) values('subtime(''9999-12-31 20:59:59'', ''839:59:59'')', subtime('9999-12-31 20:59:59', '839:59:59') );

--step4:插入subtime(time, time)参数格式且入参合法的用例执行结果;expect:成功
insert into func_test(functionName, result) values('subtime(''-37:59:59'', ''-39:59:59'')', subtime('-37:59:59', '-39:59:59') );
insert into func_test(functionName, result) values('subtime(''-37:59:59'', ''39:59:59'')', subtime('-37:59:59', '39:59:59') );
insert into func_test(functionName, result) values('subtime(''37:59:59'', ''-39:59:59'')', subtime('37:59:59', '-39:59:59') );
insert into func_test(functionName, result) values('subtime(''375959'', ''395959'')', subtime('375959', '395959') );
insert into func_test(functionName, result) values('subtime(''010000.999999'', ''020000.999998'')', subtime('010000.999999', '020000.999998'));
insert into func_test(functionName, result) values('subtime(''24:00:00.999999'', ''02:00:00.999998'')', subtime('24:00:00.999999', '02:00:00.999998'));
insert into func_test(functionName, result) values('subtime(''01:00:00.000000'', ''02:00:00.999999'')', subtime('01:00:00.000000', '02:00:00.999999'));
insert into func_test(functionName, result) values('subtime(''60:00:00.000000'', ''02:00:00.999999'')', subtime('60:00:00.000000', '02:00:00.999999'));
insert into func_test(functionName, result) values('subtime(''-375959'', ''-395959'')', subtime('-375959', '395959') );
insert into func_test(functionName, result) values('subtime(''-375959.000001'', ''-395959.000002'')', subtime('-375959.000001', '395959.000002') );
insert into func_test(functionName, result) values('subtime(-375959, 395959)', subtime(-375959, 395959) );
insert into func_test(functionName, result) values('subtime(-375959.000001, 395959.000002)', subtime(-375959.000001, 395959.000002) );
insert into func_test(functionName, result) values('subtime(NULL, ''-839:59:59'')', subtime(NULL, '-839:59:59') );
insert into func_test(functionName, result) values('subtime(''-837:59:59'', NULL)', subtime('-837:59:59', NULL) );

--step5:插入subtime(time, time)参数格式但涉及时间类型值超出范围的的用例执行结果;expect:合理报错
insert into func_test(functionName, result) values('subtime(''838:59:59'', ''-25:00'')', subtime('838:59:59', '-25:00') );
insert into func_test(functionName, result) values('subtime(''-838:59:59'', ''25:00'')', subtime('-838:59:59', '25:00') );
insert into func_test(functionName, result) values('subtime(''839:59:59'', ''837:59:59'')', subtime('839:59:59', '837:59:59') );
insert into func_test(functionName, result) values('subtime(''-837:59:59'', ''-839:59:59'')', subtime('-837:59:59', '-839:59:59') );

--step6:插入入参为特殊类型的subtime用例执行结果;expect:成功
insert into func_test(functionName, result) values('subtime(false, true)', subtime(false, true) );
insert into func_test(functionName, result) values('subtime(B''0'', B''1'')', subtime(B'0', B'1'));
insert into func_test(functionName, result) values('subtime(cast(''2000-02-28 20:59:59'' as datetime), time''-25:00'')', subtime(cast('2000-02-28 20:59:59' as datetime), time'-25:00') );
insert into func_test(functionName, result) values('subtime(date''2000-02-28'', time''-25:00'')', subtime(date'2000-02-28', time'-25:00') );
insert into func_test(functionName, result) values('subtime(time''20:59:59'', time''-25:00'')', subtime(time'20:59:59', time'-25:00') );
insert into func_test(functionName, result) values('subtime(cast(''2000-02-28 20:59:59'' as datetime), date''2000-01-01'')', subtime(cast('2000-02-28 20:59:59' as datetime), date'2000-01-01') );
insert into func_test(functionName, result) values('subtime(cast(''2000-02-28 20:59:59'' as datetime), cast(''2000-01-01 11:00:00'' as datetime))', subtime(cast('2000-02-28 20:59:59' as datetime), cast('2000-01-01 11:00:00' as datetime)));

--step7:插入非法入参时subtime执行结果;expect:合理报错
insert into func_test(functionName, result) values('subtime(''abcd'', ''-25:00'')', subtime('abcd', '-25:00') );
insert into func_test(functionName, result) values('subtime(''2000-02-28 20:59:59'', ''abcd'')', subtime('2000-02-28 20:59:59', 'abcd') );
insert into func_test(functionName, result) values('subtime(''abcd'', ''-839:59:59'')', subtime('abcd', '-839:59:59') );
insert into func_test(functionName, result) values('subtime(''-837:59:59'', ''abcd'')', subtime('-837:59:59', 'abcd') );
insert into func_test(functionName, result) values('subtime(''2007-13-31 23:59:59.999999'',''1 1:1:1.000002'')', subtime('2007-13-31 23:59:59.999999','1 1:1:1.000002'));
insert into func_test(functionName, result) values('subtime(''2007-12-40 23:59:59.999999'',''1 1:1:1.000002'')', subtime('2007-12-40 23:59:59.999999','1 1:1:1.000002'));
insert into func_test(functionName, result) values('subtime(''02:00:61.000000'', ''02:00:00.999999'')', subtime('02:00:61.000000', '02:00:00.999999'));
insert into func_test(functionName, result) values('subtime(''02:61:00.000000'', ''02:00:00.999999'')', subtime('02:61:00.000000', '02:00:00.999999'));
insert into func_test(functionName, result) values('subtime(''2000-01-01'', ''2022-01-01'')', subtime('2000-01-01', '2022-01-01') );

--step8:查看subtime函数执行结果是否正确;expect:成功
select * from func_test;

--step9:清理环境;expect:成功
drop table if exists func_test;