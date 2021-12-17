-- @testpoint: mod函数入参包含注释
select mod(555555555555/*dfwerfetre*/,89) from sys_dummy;
select mod(555555555555,89/*dfwerfetre*/) from sys_dummy;
select mod/*dfwerfetre*/(555555555555,89) from sys_dummy;
select /*dfwerfetre*/mod(555555555555,89) from sys_dummy;
select mod(555555555555,89)/*dfwerfetre*/ from sys_dummy;
