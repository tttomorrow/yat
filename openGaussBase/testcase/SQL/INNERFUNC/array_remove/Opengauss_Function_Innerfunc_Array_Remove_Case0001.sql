-- @testpoint: 一维数组时，array和element的类型一致，element存在于array中：删除数组中对应元素

--数值型
select array_remove(array[1,2,2,3], 2);
select array_remove(array[1.223,2,3.145], 3.145);
select array_remove(array[1.223,2,3.145], 3.1450);
select array_remove(array[0.3,2,3.145], 0.3);
select array_remove(array[-1.2,2,3.145], -1.2);
select array_remove(array[-1.223,-2,-3.145], -3.145);
select array_remove(array[-1.2,2,3],3.0);

--布尔型
select array_remove(array[true,false,null], 't');
select array_remove(array[TRUE,false,NULL], 'f');
select array_remove(array[true,false,null], '1');
select array_remove(array[true,false], 'yes');
select array_remove(array[FALSE,TRUE], '0');
select array_remove(array[true,false,null], 'true');

--字符型
select array_remove(array['abc','efg','null'], 'efg');
select array_remove(array['TABLE','EFG','NULL'], 'EFG');

--日期时间型
select array_remove(array[date'2010-12-10 00:00:00
',date'2010/12/10 16:40',date'2010-12-10 pst'], (date '12-10-2010'));
select array_remove(array[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'], (TIMESTAMP '12-10-2010'));

--JSON类型
select array_remove(array['{qq,123,null,true,false}'], '{qq,123,null,true,false}');