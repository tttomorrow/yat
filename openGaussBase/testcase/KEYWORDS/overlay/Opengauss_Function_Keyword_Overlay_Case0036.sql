--  @testpoint:opengauss关键字overlay(非保留)，自定义数据类型名为explain
SELECT overlay('hello' placing 'world' from 0 for 3 );

SELECT overlay('hello' placing 'world' from 1 for 3 );

SELECT overlay('hello' placing 'world' from 1 for 0 );

SELECT overlay('hello' placing 'world' from 2 for 3 );

SELECT overlay('hello' placing 'world' from 2 for -1 );


