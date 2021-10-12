-- @testpoint: 将anyarray中的所有anyelement1替换为anyelement2，当array为多维数组时，array和element的类型一致，element存在于array中：替换数组中对应元素

--二维数组
select array_replace(array[[0.1111,2,0.217,3.222,5.666],[2,1.335,8,2,3]],2.0,5.1);
select array_replace(array[['DB',NULL,'CDE'],['CD','CDE',null]],'CDE',12::text);
select array_replace(array[[false,false,false],[true,true,true]],'true','f');

--三维数组
select array_replace(array[[1,2,17,22,66],[2,35,8,2,3],[12,45,86,5,2]],2,3);
select array_replace(array[['DB',NULL,'CDE'],['CD','CDE',NULL],['cde','table','true']],'CDE',12::text);
select array_replace(array[[false,FALSE,false],[false,TRUE,false],[true,true,true]],'false','t');

--四维数组
select array_replace(array[[1,2],[35,8],[12,45],[22,2]],2,3);
select array_replace(array[['DB','CDE'],['CD','NULL'],['cde','table'],['ef','ac']],'CDE',12::text);
select array_replace(array[[false,false],[FALSE,false],[true,true],[TRUE,true]],'false','t');

--五维数组
select array_replace(array[[1,2],[35,8],[12,45],[22,2],[48,63]],2,3);
select array_replace(array[['DB','CODE'],['CD','CODE'],['code','table'],['schema','cobe'],['cdef','']],'code',12::text);
select array_replace(array[['DB','CODE'],['CD','CODE'],['code','table'],['schema','cobe'],['cdef',NULL]],'code',12::text);
select array_replace(array[['DB','CODE'],['CD','CODE'],['code','table'],['schema','cobe'],['cdef',null]],'code',12::text);