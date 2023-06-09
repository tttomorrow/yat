-- @testpoint: 删除数组array中所有的anyelement元素时,对于大小写null，空字符串的测试

select array_remove(array[1,2,2,3,null], NULL);
select array_remove(array[1,2,2,3,null], '');
select array_remove(array[1,2,2,3,null], null);
select array_remove(array[1.223,2,3.145,NULL], null);
select array_remove(array[1.223,2,3.145,NULL], NULL);
select array_remove(array[1.223,2,3.145,NULL], '');
select array_remove(array[1.223,2,3.145,''],NULL);
select array_remove(array[-1.223,'',-3.145], null);
select array_remove(array[-1.223,'',-3.145],'');
select array_remove(array[true,false,null], null);
select array_remove(array[true,false,null], NULL);
select array_remove(array[true,false,NULL], NULL);
select array_remove(array[true,false,NULL], null);
select array_remove(array['abc','efg',null], null);
select array_remove(array['abc','efg',null], NULL);
select array_remove(array['abc','efg',null], '');
select array_remove(array['abc','efg',NULL], NULL);
select array_remove(array['abc','efg',NULL],null);
select array_remove(array['abc','efg',NULL], '');
select array_remove(array['abc','efg',''], NULL);
select array_remove(array['abc','efg',''], null);
select array_remove(array['abc','efg',''], '');
select array_remove(array['abc','efg','null'], 'null');
select array_remove(array['abc','efg','NULL'], 'NULL');
select array_remove(array['abc','efg','null'], '');
select array_remove(array['abc','efg','NULL'], '');
select array_remove(array['abc','efg','null'], 'NULL');
select array_remove(array['abc','efg','NULL'], 'null');