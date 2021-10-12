-- @testpoint: array_dims函数，返回非数组各个维度中的低位下标值和高位下标值,合理报错

select array_dims(array[1,2,a]) as result;
select array_dims(array[[7,1,@], [1,3,6]]) as result;
select array_dims(array[[[7,1,2], [1,3,6],[1,5,_]]]) as result;