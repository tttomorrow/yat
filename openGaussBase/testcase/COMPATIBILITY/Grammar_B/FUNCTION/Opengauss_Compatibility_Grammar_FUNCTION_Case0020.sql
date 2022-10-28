-- @testpoint: 时间函数UTC_TIME功能测试,部分测试步骤合理报错
--step1:创建用于存储函数结果的表;expect:成功
drop table if exists func_test;
create table func_test(functionName varchar(256),result varchar(256));

--step2:插入UTC_TIME正常执行结果;expect:成功
insert into func_test(functionName, result) values('UTC_TIMESTAMP', UTC_TIMESTAMP);
insert into func_test(functionName, result) values('UTC_TIMESTAMP()', UTC_TIMESTAMP());
insert into func_test(functionName, result) values('UTC_TIMESTAMP(0)', UTC_TIMESTAMP(0));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(1)', UTC_TIMESTAMP(1));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(2)', UTC_TIMESTAMP(2));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(3)', UTC_TIMESTAMP(3));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(4)', UTC_TIMESTAMP(4));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(5)', UTC_TIMESTAMP(5));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(6)', UTC_TIMESTAMP(6));

--step3:插入非法入参下UTC_TIME执行结果;expect:合理报错
insert into func_test(functionName, result) values('UTC_TIMESTAMP(-1)', UTC_TIMESTAMP(-1));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(7)', UTC_TIMESTAMP(7));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(''1'')', UTC_TIMESTAMP('1'));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(True)', UTC_TIMESTAMP(True));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(b''1'')', UTC_TIMESTAMP(b'1'));
insert into func_test(functionName, result) values('UTC_TIMESTAMP(null)', UTC_TIMESTAMP(null));

--step4:查看UTC_TIME函数执行结果是否正确;expect:成功
select * from func_test;

--step5:清理环境;expect:成功
drop table if exists func_test;