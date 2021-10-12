-- @testpoint: 将anyarray中的所有anyelement1替换为anyelement2，当array为多维数组时，array和element的类型不一致，合理报错

--二维数组
select array_replace(array[[223,2,3,145],[1,2,3,14]],2.0,8.6);
select array_replace(array[[0.3,2,3.145],[0.217,3.2,5.6]],2,3.8);
select array_replace(array[['123',NULL,'CDE'],['12','CDE',null]],('12'::int),12::text);
select array_replace(array[[false,false,false],[false,false,false]],('true'::char),'f');

--三维数组
select array_replace(array[[1,2,17,22,66],[2,35,8,2,3],[12,45,86,5,2]],25.0,3);
select array_replace(array[['DB',NULL,'CDE'],['CD','CDE',NULL],['cde','table','true']],true,12::text);
select array_replace(array[[false,FALSE,false],[false,false,false],[false,false,false]],('true'::char),'f');

--四维数组
select array_replace(array[[1,2],[35,8],[12,45],[22,2]],2.0,3);
select array_replace(array[['DB','CDE'],['CD','NULL'],['cde','table'],['ef','ac']],23,12::text);
select array_replace(array[[false,false],[FALSE,false],[false,false],[FALSE,false]],('t'::char),'f');

--五维数组
select array_replace(array[[1,2],[35,8],[12,45],[22,2],[48,63]],7.0,3);
select array_replace(array[['DB','CODE'],['CD','CODE'],['code','table'],['schema','cobe'],['cdef','']],158,12::text);
select array_replace(array[['DB','CODE'],['CD','CODE'],['code','table'],['schema','cobe'],['cdef',NULL]],742,12::text);
select array_replace(array[['DB','CODE'],['CD','CODE'],['code','table'],['schema','cobe'],['cdef',null]],true,12::text);
select array_replace(array[[true,true],[TRUE,true],[TRUE,true],[TRUE,null],[true,true]],('false'::char),'t');
