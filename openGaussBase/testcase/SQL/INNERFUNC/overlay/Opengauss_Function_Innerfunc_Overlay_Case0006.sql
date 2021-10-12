-- @testpoint: overlay函数参数为负数或者浮点型,from为负数时合理报错
SELECT overlay('hello' placing 'world' from 2 for -3 );
SELECT overlay('hello' placing 'world' from 2 for -3.6 );
SELECT overlay('hello' placing 'world' from 2.1 for 3 );
SELECT overlay('hello' placing 'world' from 2.1 for 3.4 );
SELECT overlay('hello' placing 'world' from -2 for -3 );
SELECT overlay('hello' placing 'world' from -2 for 3 );

