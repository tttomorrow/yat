-- @testpoint: 参数为负数,正数,正负数结合
select nullif(-0.45, 0.45);
select nullif(-0.12,-0.12);
select nullif(0.12,-0.12);
select nullif(1.0,1.00);
select nullif(-1.0,-1.00);
select nullif(-1.120,-1.12);