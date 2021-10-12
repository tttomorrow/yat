-- @testpoint: 字符处理函数translate，入参为数组类型_数组元素时合理报错

select translate(array['100123','22212'],'10','真假');
