-- @testpoint: 一维数组时，array和element的类型一致，element不存在于array中:不做操作，返回array
--数值型
select array_remove(array[1,2,2,3], 4);
select array_remove(array[1.223,2,3.145], 3.14);
select array_remove(array[0.3,2,3.145], 2.3);
select array_remove(array[-1.2,2,3.145], -1.22);
select array_remove(array[-1.223,-2,-3.145], 3.145);
select array_remove(array[-1.2,2,3],-3.0);

--布尔型
select array_remove(array[true,null], 'n');
select array_remove(array[false,null], 'T');
select array_remove(array[TRUE,null], 'false');
select array_remove(array[FALSE,NULL], 'true');
select array_remove(array[FALSE,false], 'yes');
select array_remove(array[true,TRUE], '0');

--字符型
select array_remove(array['abc','efg','null'], 'ab');
select array_remove(array['abc','efg','null'], 'efgh');

--日期时间型
select array_remove(array[date'2010-12-10 00:00:00
',date'2010/12/10 16:40',date'2010-12-10 pst'], (date '11-10-2010'));
select array_remove(array[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'], (TIMESTAMP '12-10-2010 18:00'));

--JSON类型
select array_remove(array['{qq,123,null,true,false}'], '{qq,123,true,false}');