-- @testpoint: nvl函数俩参数同时为null
select nvl(null,null);
select nvl(null+1-2*3/4,null);