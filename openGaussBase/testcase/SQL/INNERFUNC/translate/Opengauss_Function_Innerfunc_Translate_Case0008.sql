-- @testpoint: 字符处理函数translate，入参参数个数少于3，合理报错

select translate('ａAbc','一二三四');
select translate('ａAbc');

