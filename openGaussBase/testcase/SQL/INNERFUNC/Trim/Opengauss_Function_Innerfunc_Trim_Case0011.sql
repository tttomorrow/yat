-- @testpoint: 字符处理函数trim，入参参数1/参数2无输入，没有参数2时合理报错

select trim(both '2' from );
select trim(leading'2' from );
select trim(trailing '2' from );
select trim(trailing from '245892');
select trim(leading from '245892');
select trim(both from '245892');
