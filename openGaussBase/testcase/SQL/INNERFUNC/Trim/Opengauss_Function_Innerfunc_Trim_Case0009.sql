-- @testpoint: 字符处理函数trim，入参中无关键字from，入参中不限制leading/trailing/both时合理报错

select trim('2' '298082');
select trim(both '749832');
select trim(leading '79879823');
select trim(trailing '979dsj');
