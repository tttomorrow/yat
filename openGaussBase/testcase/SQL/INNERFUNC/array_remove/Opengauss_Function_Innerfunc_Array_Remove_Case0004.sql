-- @testpoint: 多维数组时，Array_remove(anyarray, anyelement) ：不支持，合理报错

--数值型
select array_remove('{{1,2,2},{1,4,3}}',2);
select array_remove(array[[1,2,2,3],[0.3,2,3.145]],'2');
select array_remove(array[[-1.2,2,3.145],[-1.223,-2,-3.145]],'-1.2');

--布尔型
select array_remove(array[[true,false,null],[true,false,null]],'0');
select array_remove(array[[TRUE,false,null],[true,false,null]],'t');
select array_remove(array[[true,false,null],[FALSE,null,true]],'0');
select array_remove(array[[true,FALSE,true,false],[TRUE,false,null,true]],'t');

--字符型
select array_remove(array[['123','efg','null'],['true','false','null']], '{123,efg,null}');
select array_remove(array[['123','efg','null'],['true','false','null']], '[123,efg,null]');

--日期时间型
select array_remove(array[[date'2010-12-10 00:00:00
',date'2010/12/10 16:40',date'2010-12-10 pst'],[date'2020-12-10 00:00:00
',date'2020/12/10 16:40',date'2020-12-10 pst']], (TIMESTAMP '12-10-2010'));
select array_remove(array[[TIMESTAMP'2010-12-10 00:00:00
',TIMESTAMP'2010/12/10 16:40',TIMESTAMP'2010-12-10 pst'],[TIMESTAMP'2020-12-10 00:00:00
',TIMESTAMP'2020/12/10 16:40',TIMESTAMP'2020-12-10 cst']],(date '12-10-2010'));

--JSON类型
select array_remove(array[['{qq,123,null,true,false}'],['{qq,123,null,true,false}']], '[qq,123,null,true,false]');
select array_remove(array[['{qq,123,null,true,false}'],['{qq,123,null,true,false}']], 'text([qq,123,null,true,false])');
select array_remove(array[['{qq,123,null,true,false}'],['{qq,123,null,true,false}']], 'int([qq,123,null,true,false])');
select array_remove(array[['{qq,123,null,true,false}'],['{qq,123,null,true,false}']], 'varchar([qq,123,null,true,false])');
