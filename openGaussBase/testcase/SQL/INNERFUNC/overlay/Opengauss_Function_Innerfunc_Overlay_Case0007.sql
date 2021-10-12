-- @testpoint: overlay函数多参少参校验，合理报错
SELECT overlay('hello' placing  from 2 for -3 );
SELECT overlay('hello' placing 'world' from 2 for -3  for 4);
