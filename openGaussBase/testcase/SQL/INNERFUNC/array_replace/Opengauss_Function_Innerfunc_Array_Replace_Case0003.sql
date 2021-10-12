-- @testpoint: 将anyarray中的所有anyelement1替换为anyelement2，当array为一维数组时，array和element的类型不一致，部分合理报错

--数值型
select array_replace(array[1.223,2,3.145],'2.0',8.6);
select array_replace(array[0.3,2,3.145],'0.30',3.8);
select array_replace(array[-1.223,-2,-3.145], '-3.1457',4.5);
select array_replace(array[-1.2,2,3],'2',3.333);
select array_replace(array[1,2,2,3], '2.0',5);
select array_replace(array[-1.2,2,3.145], (2::text),5.6);

--布尔型
select array_replace(array[true,false,null],'false'::int,false);
select array_replace(array[true,false,NULL],'true'::char,'f');
select array_replace(array[true,false,null],'yes'::text,'1');
select array_replace(array[TRUE,FALSE],'no'::varchar,'yes');
select array_replace(array[TRUE,FALSE,true,false,null],1,'0');
select array_replace(array[TRUE,FALSE,true,false],0,'1');

--字符型
select array_replace(array['abc','efg','null'],123,'qaz');
select array_replace(array['abc','efg','NULL'],TRUE,'database');

--日期时间型
select array_replace(array[date'2010-12-10 00:00:00
',date'2010/12/10 16:40',date'2010-12-10 pst'],(timestamp without time zone'2021-12-10'),(date '08-10-2020'));
select array_replace(array[date'2010-12-10 00:00:00
',date'2010/12/10 16:40',date'2010-12-10 pst'],(2021-12-10 ::text),(date '08-10-2020'));
select array_replace(array[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'],((2021-12-10 ::varchar)),(TIMESTAMP '08-02-2020'));

--JSON类型
select array_replace(array['{qq,123,null,true,false}'],(select('qq',123,NULL,true,false)::text),'{database,table,view,schema,index}');
select array_replace(array['{12,123,1234,12345,678}'],(select '{"12","123","1234","12345","678"}'::varchar),'{database,table,view,schema,index}');