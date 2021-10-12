-- @testpoint: 将anyarray中的所有anyelement1替换为anyelement2，当array为多维数组时，array和element的类型一致，element不存在于array中：不做操作，返回array

--二维数组
select array_replace(array[[0.1111,2,0.217,3.222,5.666],[2,1.335,8,2,3]],2.14,5.1);
select array_replace(array[['DB',NULL,'CDE'],['CD','CDE',null]],'BC',12::text);
select array_replace(array[[false,false,false],[false,false,false]],'true','f');

--三维数组
select array_replace(array[[1,2,17,22,66],[2,35,8,2,3],[12,45,86,5,2]],25,3);
select array_replace(array[['DB',NULL,'CDE'],['CD','CDE',NULL],['cde','table','true']],'CDEF',12::text);
select array_replace(array[[false,FALSE,false],[false,false,false],[false,false,false]],'TRUE','f');

--四维数组
select array_replace(array[[1,2],[35,8],[12,45],[22,2]],4,3);
select array_replace(array[['DB','CDE'],['CD','NULL'],['cde','table'],['ef','ac']],'CDEF',12::text);
select array_replace(array[[false,false],[FALSE,false],[false,false],[FALSE,false]],'t','f');

--五维数组
select array_replace(array[[1,2],[35,8],[12,45],[22,2],[48,63]],7,3);
select array_replace(array[['DB','CODE'],['CD','CODE'],['code','table'],['schema','cobe'],['cdef','']],'co',12::text);
select array_replace(array[['DB','CODE'],['CD','CODE'],['code','table'],['schema','cobe'],['cdef',NULL]],'ode',12::text);
select array_replace(array[['DB','CODE'],['CD','CODE'],['code','table'],['schema','cobe'],['cdef',null]],'cod',12::text);
select array_replace(array[[true,true],[TRUE,true],[TRUE,true],[TRUE,null],[true,true]],'false','no');