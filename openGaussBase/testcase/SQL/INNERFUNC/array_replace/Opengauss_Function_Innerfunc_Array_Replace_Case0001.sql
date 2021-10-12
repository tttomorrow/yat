-- @testpoint: 将anyarray中的所有anyelement1替换为anyelement2，当array为一维数组时，array和element的类型一致，element存在于array中：替换数组中对应元素

--数值型
select array_replace(array[1,2,2,3], 2,5);
select array_replace(array[1.223,2,3.145], 3.145,8.6);
select array_replace(array[1.223,2,3.145], 3.1450,3.33);
select array_replace(array[0.3,2,3.145], 0.3,3.8);
select array_replace(array[-1.2,2,3.145], -1.2,5.6);
select array_replace(array[-1.223,-2,-3.145], -3.145,4.5);
select array_replace(array[-1.2,2,3],3.0,3.333);

--布尔型
select array_replace(array[true,false,null],'t',false);
select array_replace(array[true,false,NULL],'T','f');
select array_replace(array[true,false,null],'0','1');
select array_replace(array[TRUE,FALSE],'false','yes');
select array_replace(array[TRUE,FALSE,true,false,null],TRUE,'0');
select array_replace(array[TRUE,FALSE,true,false],'no','1');

--字符型
select array_replace(array['abc','efg','null'],'efg','qaz');
select array_replace(array['abc','efg','NULL'],'EFG','database');

--日期时间型
select array_replace(array[date'2010-12-10 00:00:00
',date'2010/12/10 16:40',date'2010-12-10 pst'],(date'2010-12-10 00:00:00'),(date '08-10-2020'));
select array_replace(array[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'],(date'2010-12-10 00:00:00'),(TIMESTAMP '08-02-2020'));

--JSON类型
select array_replace(array['{qq,123,null,true,false}'],'{qq,123,null,true,false}','{database,table,view,schema,index}');