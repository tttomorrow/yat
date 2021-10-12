-- @testpoint: opengauss内置函数length，作为函数名 合理报错

select length(1::tsvector);