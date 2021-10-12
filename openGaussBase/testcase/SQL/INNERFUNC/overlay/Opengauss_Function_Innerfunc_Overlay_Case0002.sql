-- @testpoint: overlay函数替换个数为负数
SELECT overlay('hello' placing 'world' from 2 for -3 );