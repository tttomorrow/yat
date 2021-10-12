-- @testpoint: 字符处理函数trim，参数中包含特殊字符

select trim(leading '~1' from '~1gdf89$56@kvo1');
select trim(both '~1' from '~1gdf89$56@kvo1');
select trim(trailing '~1' from 'cdsf8fiue#^~1');
