-- @testpoint: 将anyarray中的所有anyelement1替换为anyelement2，当array为一维数组时，array和element的类型一致，element不存在于array中：不做操作

--数值型
select array_replace(array[1,2,2,3], 4,5);
select array_replace(array[1.223,2,3.145], 3.1451,8.6);
select array_replace(array[0.3,2,3.145], 0.32,3.8);
select array_replace(array[-1.2,2,3.145], -1.22,5.6);
select array_replace(array[-1.223,-2,-3.145], -3.1457,4.5);
select array_replace(array[-1.2,2,3],3.01,3.333);

--布尔型
select array_replace(array[false,false,null],'t',false);
select array_replace(array[FALSE,false,NULL],'T','f');
select array_replace(array[true,true,null],'0','1');
select array_replace(array[TRUE,TRUE],'false','yes');
select array_replace(array[false,FALSE,false,false,null],TRUE,'0');
select array_replace(array[TRUE,TRUE,true,true],'no','1');

--字符型
select array_replace(array['abc','efg','null'],'efgh','qaz');
select array_replace(array['abc','efg','NULL'],'EFGH','database');

--日期时间型
select array_replace(array[date'2010-12-10 00:00:00
',date'2010/12/10 16:40',date'2010-12-10 pst'],(date'2021-12-10 00:00:00'),(date '08-10-2020'));
select array_replace(array[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'],(date'2021-12-10 00:00:00'),(TIMESTAMP '08-02-2020'));

--JSON类型
select array_replace(array['{qq,123,null,true,false}'],'{QQ,123,NULL,true,false}','{database,table,view,schema,index}');
select array_replace(array['{12,123,1234,12345,678}'],'{12,123,1234,12345}','{database,table,view,schema,index}');
select array_replace(array['{pg,gs,mysql,oracle}'],'{oracle,mysql,gs,pg}','{database,table,view,schema,index}');