-- @testpoint: 将小数先转化为货币类型再由货币类型转换为小数类型

select '52093.89'::money::numeric::float8;

