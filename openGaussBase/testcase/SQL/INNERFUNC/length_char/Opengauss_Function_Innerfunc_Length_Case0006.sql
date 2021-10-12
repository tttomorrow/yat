-- @testpoint: 字符处理函数length嵌套的输入测试
select length(concat('sgdgdgdsgdsgfdgd','sgfdgdgfg')) from sys_dummy;
select length(HEXTORAW('abcdef')) from sys_dummy;

