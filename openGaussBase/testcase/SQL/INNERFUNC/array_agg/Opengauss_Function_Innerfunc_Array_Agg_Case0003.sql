-- @testpoint: array_agg函数中输入数组类型的值，合理报错
select array_agg(array[342321,5454]) from sys_dummy;
select array_agg('{12312,4535fdgdfg,fghgfhkhjsddfre}') from sys_dummy;