-- @testpoint: 基础测试点(空值,参数个数)
select nullif('','');
select nullif(' ',' ');
select nullif('  ',' ');
SELECT NULLIF(1,1);
SELECT NULLIF(2,3);
SELECT NULLIF(NULL,1);
select nullif(1,null);
select NULLIF(,);
select NULLIF();