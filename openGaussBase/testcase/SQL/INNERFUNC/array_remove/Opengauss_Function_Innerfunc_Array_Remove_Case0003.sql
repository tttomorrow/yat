-- @testpoint: 一维数组时，array和element的类型不一致,但存在隐式数据类型转换，部分合理报错

--数值型
select array_remove(array[1,2,2,3], '2');
select array_remove(array[1.223,2,3.145], '3.145');
select array_remove(array[1.223,2,3.145], '3.1450');
select array_remove(array[0.3,2,3.145], '0.3');
select array_remove(array[-1.2,2,3.145], '-1.2');
select array_remove(array[-1.223,-2,-3.145], '-3.145');
select array_remove(array[-1.2,2,3],'3.0');
select array_remove(array[-1.2,2,3.14],2);
select array_remove(array[-1.2,2,-3.14],2);
select array_remove(array[-1.2,-2,-3.14],-2);

--布尔型
select array_remove(array[true,false,null], 1);
select array_remove(array[true,false,null], 0);
select array_remove(array[true,FALSE,null], '{true}');
select array_remove(array[TRUE,false,null], 1::text);
select array_remove(array[true,false,null], 0::char);
select array_remove(array[true,false,null], 23);

--字符型
select array_remove(array['123','efg','null'], '{123,efg,null}');
select array_remove(array['123','efg','null'], 123);

--日期时间型
select array_remove(array[date'2010-12-10 00:00:00
',date'2010/12/10 16:40',date'2010-12-10 pst'], (TIMESTAMP '12-10-2010'));
select array_remove(array[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'], (date '12-10-2010'));
select array_remove(array[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'],  '12-10-2010');
select array_remove(array[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'],  '12102010 ');
select array_remove(array[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'],  '12.10.2010 ');
select array_remove(array[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'],  '2010.10.10 18:00 cst');

--JSON类型
select array_remove(array['{qq,123,null,true,false}'], '[qq,123,null,true,false]');
select array_remove(array['{qq,123,null,true,false}'], '[qq,123,null,true,false]::text');
select array_remove(array['{qq,123,null,true,false}'], '([qq,123,null,true,false]::int)');
select array_remove(array['{qq,123,null,true,false}'], '([qq,123,null,true,false]::varcahr)');
