-- @testpoint: 参数为特殊字符
select nullif(#,&) from sys_dummy;
select nullif(#,#) from sys_dummy;
select nullif((,)) from sys_dummy;
select nullif(@,@) from sys_dummy;
select nullif(+,-) from sys_dummy;
select nullif(!,~) from sys_dummy;