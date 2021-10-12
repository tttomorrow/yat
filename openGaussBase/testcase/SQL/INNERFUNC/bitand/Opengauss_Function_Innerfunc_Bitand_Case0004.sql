-- @testpoint: 输入无效参数(合理报错)

select bitand(6) as result from sys_dummy;
select bitand(6,) as result from sys_dummy;
select bitand(,6) as result from sys_dummy;
select bitand(6,0,1) as result from sys_dummy;
select bitand() as result from sys_dummy;
