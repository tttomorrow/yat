-- @testpoint: overlay函数入参为空字符、null、空格
SELECT overlay('' placing 'world' from 2 for -3 );
SELECT overlay(' ' placing 'world' from 2 for -3 );
SELECT overlay(null placing 'world' from 2 for -3 );
